# your_app/management/commands/clear_test_data.py
from django.core.management.base import BaseCommand
from zcglxt.models import Data_All,Edit_Log,Departments,Type_Names
 
class Command(BaseCommand):
    help = 'Clears all test data'
    def handle(self, *args, **options):
        Data_All.objects.all().delete()
        Edit_Log.objects.all().delete()
        Departments.objects.all().delete()
        Type_Names.objects.all().delete()