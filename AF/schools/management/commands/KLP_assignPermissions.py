from django.core.management.base import BaseCommand, CommandError
from schools.models import *
import django, datetime, os, csv
from AkshararestApi.KLP_Permission import assignPermission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
	''' Command To Assign Permissions to the User.''' 
	def handle(self, *args, **options):
		try:
			# Reads the arguments from command line.
			objsFileName = args[0]
			usersFileName = args[1]
			assessmentPerm = True
			permissions = ['Acess']
			permissionType = 'permissions'
			assessmentId = None
			if objsFileName and usersFileName:
				try:
					boundaryFile = open(objsFileName, 'r')
					boundaryIds = boundaryFile.read().replace('\n', '')  # read data from file
					boundaryFile.close()
					userFile = open(usersFileName, 'r')
					userIds = userFile.read().replace('\n', '')  # read data from file
					userFile.close()
					boundaryIdsList = boundaryIds.split(',')
					userIdsList = userIds.split(',')
					for bId in boundaryIdsList:
						inst_list = Institution.objects.filter(boundary__parent__id = bId, active=2).values_list('id', flat=True).distinct() 
						asmIdList = assignPermission(inst_list, userIdsList, permissions, permissionType, assessmentId, assessmentPerm)
						self.stdout.write("Assigned Permissions successfully for %s Institutions  and %s Assessments Assigned successfully \n" %(inst_list.count(), len(asmIdList)))
					
				except:
					raise CommandError('Pass First Parameter as Boundary Ids List file and Second Parameter as User Ids List \n')
			else:
				raise CommandError('Pass Use Ids List and Boundary Ids List files \n')
		except:
			raise CommandError('Pass First Parameter as Boundary Ids List file and Second Parameter as User Ids List \n')
			
			
			
