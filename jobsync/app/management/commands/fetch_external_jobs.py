import json
from django.core.management.base import BaseCommand
from jobsync.app.models import JobListing, Organisation
from django.utils import timezone

class Command(BaseCommand):
    help = "Populate job listings from weworkremotely_jobs_by_category.json"

    def handle(self, *args, **kwargs):
        try:
            # Load JSON data
            with open('weworkremotely_jobs_by_category.json', 'r') as f:
                jobs = json.load(f)

            # Track success/failure
            created_count = 0
            error_count = 0

            for job in jobs:
                try:
                    # Get or create organisation
                    org_name = job.get('company', '').strip()
                    if not org_name:
                        continue
                        
                    organisation, _ = Organisation.objects.get_or_create(
                        name=org_name
                    )

                    # Create job listing
                    JobListing.objects.create(
                        title=job.get('title'),
                        company=organisation,
                        location=job.get('location'),
                        description=job.get('description', ''),
                        external_url=job.get('external_url'),
                        posted_at=timezone.now()
                    )
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error creating job: {str(e)}')
                    )
                    error_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_count} job listings with {error_count} errors'
                )
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Could not find weworkremotely_jobs_by_category.json')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Invalid JSON format in data file')
            )