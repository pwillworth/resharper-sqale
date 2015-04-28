# This utility script compares a sonar rules export to the sqale model file
# If any rules in the sqale model are not in the rules export, they are removed from sqale model
# If any rules in the export are not in the sqale model, they are added to the sqale model
# finally, the new resulting sqale model is written over the old one

import xml.dom.minidom

modelDOM = xml.dom.minidom.parse('resharper-model.xml')
rulesDOM = xml.dom.minidom.parse('cs-resharper-all-77055.xml')


def addKeyBlock(keyName):
	keyBlock = modelDOM.createElement('chc')
	ruleKey = modelDOM.createElement('rule-key')
	keyText = modelDOM.createTextNode(keyName)
	characteristic = modelDOM.createElement('characteristic')
	subCharacteristic = modelDOM.createElement('sub-characteristic')
	prop = modelDOM.createElement('prop')
	key = modelDOM.createElement('key')
	kt = modelDOM.createTextNode('remediationFactor')
	val = modelDOM.createElement('val')
	txt = modelDOM.createElement('txt')
	tt = modelDOM.createTextNode('min/h/d')
			
	sqaleElement = modelDOM.getElementsByTagName('sqale')[0]
	sqaleElement.appendChild(keyBlock)
	keyBlock.appendChild(ruleKey)
	ruleKey.appendChild(keyText)
	keyBlock.appendChild(characteristic)
	keyBlock.appendChild(subCharacteristic)
	keyBlock.appendChild(prop)
	prop.appendChild(key)
	key.appendChild(kt)
	prop.appendChild(val)
	prop.appendChild(txt)
	txt.appendChild(tt)

def removeOldRules():
	oldRuleKeys = modelDOM.getElementsByTagName('rule-key')
	newRuleKeys = rulesDOM.getElementsByTagName('key')
	for node in oldRuleKeys:
		keyFound = False
		for nnode in newRuleKeys:
			if node.firstChild.data == nnode.firstChild.data:
				keyFound = True
				break

		if keyFound == False:
			keyBlock = node.parentNode
			modelDOM.documentElement.removeChild(keyBlock)
			print('Deleted Key {0} becuase it was not found in new rules list.'.format(node.firstChild.data))

def addNewRules():
	oldRuleKeys = modelDOM.getElementsByTagName('rule-key')
	newRuleKeys = rulesDOM.getElementsByTagName('key')
	for node in newRuleKeys:
		keyFound = False
		for nnode in oldRuleKeys:
			if node.firstChild.data == nnode.firstChild.data:
				keyFound = True
				break

		if keyFound == False:
			addKeyBlock(node.firstChild.data)
			print('Added Key {0} becuase it was not found in old sqale.'.format(node.firstChild.data))

removeOldRules()
addNewRules()

result = modelDOM.toxml('utf-8')
# The default toprettyxml does not actually end up very pretty so some help is needed
reparsed = xml.dom.minidom.parseString(result)
reprettied = '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2, encoding='utf-8').split('\n') if line.strip()])
# Expand elements that get abreviated by default so it's less work to add values for them.
renormaled = reprettied.replace('<characteristic/>','<characteristic></characteristic>').replace('<sub-characteristic/>','<sub-characteristic></sub-characteristic>').replace('<val/>','<val></val>')
f = open('resharper-model.xml', 'w')
f.write(renormaled)
f.close()
