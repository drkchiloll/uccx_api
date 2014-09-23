from sys import argv
from getpass import getpass
from lxml import etree
from lxml.etree import tostring
from optparse import OptionParser
import requests
grplist_doc = None

def get_grpdoc():
	global grplist_doc
	r1 = requests.get(url,auth=(user,pwd))
	grplist_doc = etree.XML(r1.content)
	#print etree.tostring(grplist_doc,pretty_print=True)

def add_newrsrcgrp(data):
	r1 = requests.post(url,headers=headers,data=data,auth=(user,pwd))
	return r1.status_code

def modify_rsrcgrp(uri,data):
	r1 = requests.put(uri,headers=headers,data=data,auth=(user,pwd))
	#print r1.content
	return r1.status_code

def delete_rsrcgrp(grp):
	refuri = etree.XPath('//*[name[.="'+grp+'"]]/self/text()')
	refuri = refuri(grplist_doc)[0]
	r1 = requests.delete(refuri, auth=(user,pwd))
	return r1.status_code

def rsrcgrp_doc(action,cur_grp,new_grp):
	doc = etree.Element('ResourceGroup')
	self_e = etree.SubElement(doc,'self')
	if action == 'modify':
		refuri = etree.XPath('//*[name[.="'+cur_grp+'"]]/self/text()')
		try:
			refuri = refuri(grplist_doc)[0]
			self_e.text = refuri
			id_e = etree.SubElement(doc,'id')
			id_e.text = refuri[-1:]
			cur_grp = new_grp
		except IndexError:
			#Document Format Error
			print 'Error in the CSV. ',
			print 'Moving to next RG.'
			return None
	name_e = etree.SubElement(doc,'name')
	name_e.text = cur_grp
	#print etree.tostring(doc,pretty_print=True)
	if action == 'add':
		return add_newrsrcgrp(etree.tostring(doc,pretty_print=True))
	else:
		return modify_rsrcgrp(refuri, etree.tostring(doc,pretty_print=True))

def main():
	global url,headers,user,pwd
	parser = OptionParser()
	parser.add_option('-f',dest='input_file',help='CSV Path + FileName')
	(options,args) = parser.parse_args()
	ipaddr = raw_input('PLease Enter the CCX Servers IP Address or Hostname. ')
	user = raw_input('Please enter your username. ')
	pwd = getpass('Enter your password. ')
	url = 'http://%s/adminapi/resourceGroup' % ipaddr
	headers = {'content-type':'text/xml'}

	#First Get the ResourceGroup Document
	get_grpdoc()

	if options.input_file:
	    input_file = options.input_file
	f = open(input_file,'rb')

	csv_file = f.read()
	csv_file = csv_file.split('\r\n')
	csv_header = csv_file[0]
	csv_file.remove(csv_header)
	# print csv_file
	for grp_conf in csv_file:
		grp_list = grp_conf.split(',')
		rsrcGrp = grp_list[0]
		try:
			if 't' in grp_list[1]:
				print 'Attempting to add the %s RG.' % rsrcGrp
				result = rsrcgrp_doc('add',rsrcGrp,'')
				if result == 201:
					print '%s was added successfully.' % rsrcGrp
			#When Modifying a ResourceGroup you are just changing the Name
			#So You probably Won't See this Very Often..?
			elif 't' in grp_list[2]:
				print 'Modify %s' % rsrcGrp
				#Last Element in the List
				rsrcGrpMod = grp_list[-1]
				result = rsrcgrp_doc('modify',rsrcGrp,rsrcGrpMod)
				if result == 200:
					print '%s was modified successfully.' % rsrcGrp
			#Delete the Resource Group
			elif 't' in grp_list[3]:
				result = delete_rsrcgrp(rsrcGrp)
				if result == 200:
					print '%s was deleted successfully.' % rsrcGrp
		except IndexError:
		    continue
if __name__=='__main__':
	main()