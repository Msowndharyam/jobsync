from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Count, Q , Avg
from ..models import User, JobListing, JobApplication
from .serializers import UserSerializer, JobListingSerializer, JobApplicationSerializer, SignInSerializer, JobRecommendationSerializer
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSerializer
        if self.action == 'signin':
            return SignInSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['post'], url_path='signup')
    def signup(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")
        job_title = request.data.get("job_title")

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create(
            name=name,
            email=email,
            role=role,
            job_title=job_title
        )
        user.set_password(password)
        user.save()
            
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User registered successfully.",
            "token": token.key,
            "user": {
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "job_title": user.job_title
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='signin')
    def signin(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful.",
                "token": token.key,
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "job_title": user.job_title
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

class JobListingViewSet(viewsets.ModelViewSet):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def employer_insights(self, request):
        print(f"User role: {request.user.role}")
        print(f"User organisation: {request.user.organisation}")
        
        if request.user.role != 'recruiter':
            return Response(
                {"detail": "Unauthorized - must be recruiter"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not request.user.organisation:
            return Response(
                {"detail": "No organisation associated with user"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        jobs = JobListing.objects.filter(
            company=request.user.organisation
        ).annotate(
            total_applications=Count('applications')
        )
        
        total_jobs = jobs.count()
        most_popular_job = jobs.order_by('-total_applications').first()
        
        print(f"Total jobs found: {total_jobs}")
        print(f"Most popular job: {most_popular_job.title if most_popular_job else None}")

        return Response({
            "total_jobs": total_jobs,
            "most_popular_job": most_popular_job.title if most_popular_job else None,
            "organisation": request.user.organisation.name,
            "job_stats": {
                "total_applications": sum(job.total_applications for job in jobs),
                "average_applications": jobs.aggregate(Avg('total_applications'))['total_applications__avg']
            }
        })
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        if request.user.role == 'job_seeker':
            applied_jobs = request.user.applications.all()
            recommended_jobs = JobListing.objects.filter(
                title__icontains=request.user.job_title
            )
            return Response({
                "applied_jobs": JobApplicationSerializer(applied_jobs, many=True).data,
                "recommended_jobs": JobListingSerializer(recommended_jobs, many=True).data,
            })

        elif request.user.role == 'recruiter':  # Changed from 'Recruiter' to 'recruiter'
            # Get jobs posted by the recruiter's organization
            jobs = JobListing.objects.filter(company=request.user.organisation)
            applications = JobApplication.objects.filter(job__in=jobs)
            
            print(f"User: {request.user.email}, Role: {request.user.role}")
            print(f"Organisation: {request.user.organisation}")
            print(f"Jobs found: {jobs.count()}")
            print(f"Applications found: {applications.count()}")

            return Response({
                "jobs_posted": JobListingSerializer(jobs, many=True).data,
                "applications_received": JobApplicationSerializer(applications, many=True).data,
            })

        return Response(
            {"detail": "Unauthorized - must be job seeker or recruiter"}, 
            status=status.HTTP_403_FORBIDDEN
        )

class RecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='recommendations')
    def recommendations(self, request):
        if request.user.role != 'job_seeker':
            print(f"Access denied for user: {request.user.email}, role: {request.user.role}")

            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        job_title = request.user.job_title

        # Filter job listings based on required skills and job title
        recommended_jobs = JobListing.objects.filter(
            Q(title__icontains=job_title) |
            Q(description__icontains=job_title)
        ).distinct()

        serializer = JobListingSerializer(recommended_jobs, many=True)
        return Response(serializer.data)
