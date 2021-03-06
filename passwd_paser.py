"""
Guess password from locked password crates

Use dots on unknown characters, length must match
Example:
.e.e. -> seven
a...e -> apple
..lli..ic. -> ballistic
"""

import re

pool = '''five@=acorn@,acute@,aloha@,alone@,along@,amber@,apple@,bongo@,beeps@,buddy@,clock@,crass@,crime@,crumb@,crypt@,cubed@,daunt@,death@,deter@,diary@,djinn@,drain@,drops@,easel@,earns@,flame@,flute@,freak@,ghost@,gloom@,group@,hello@,horse@,ideal@,igloo@,jumps@,jazzy@,kills@,knife@,lapis@,later@,leaps@,maybe@,mouth@,murky@,night@,noose@,odors@,opine@,piled@,prick@,prism@,queen@,quote@,rainy@,rules@,sarin@,space@,stars@,sting@,scary@,trine@,tread@,tryst@,urine@,umbra@,union@,unary@,value@,vices@,video@,where@,wring@,weepy@,wonky@,worst@,xenia@,xenon@,xerox@,yells@,yodel@,young@,youth@,yurts@,zebra@,zesty@,zilch@,zonal@,zooms
seven@=abalone@,abandon@,aerobic@,buckled@,buddies@,bottoms@,crackle@,capital@,dankest@,dissent@,earplug@,elysian@,eternal@,expunge@,exploit@,fateful@,foxtrot@,fuchsia@,gaseous@,gazelle@,gimmick@,goodbye@,heinous@,hellbox@,hypoxia@,ideally@,isolate@,jacuzzi@,jesting@,jughead@,junkies@,katydid@,knavish@,lacquer@,lateral@,lettuce@,lexicon@,lurking@,married@,mugwort@,mummify@,neither@,nucleus@,octopus@,outside@,paprika@,pumpkin@,recycle@,rejoice@,rummage@,sadness@,satchel@,shamble@,tadpole@,treetop@,uncoded@,upstart@,valiant@,veering@,volcano@,wannabe@,windbag@,yawning@,younger@,zipping@,zygotes
nine@=alongside@,andromeda@,apathetic@,ballistic@,benchmark@,blackmail@,blasphemy@,centurion@,checkmate@,chubbiest@,cosmonaut@,demagogue@,dignified@,dubiously@,emergency@,existence@,firetruck@,fruitless@,grayscale@,gunpowder@,hairbrush@,hyperlink@,impulsive@,insidious@,jumpsuits@,jitterbug@,kingmaker@,knockdown@,legendary@,lumbering@,manticore@,mausoleum@,mutations@,nightclub@,numbskull@,otherness@,pantomime@,phenotype@,pistachio@,quickness@,quadratic@,racketeer@,reinstall@,scripture@,spearfish@,tantalize@,thinkable@,trappings@,uncovered@,upwelling@,verminous@,visualize@,volunteer@,whitewash@,worksheet@,wuthering@,wrestling@,wuthering@,xylophone@,yodellers@,zookeeper@,zucchinis'''

pool = pool.splitlines()

passwd_list = []

for row in pool:
    _, values = row.split("@=")
    passwd_list += values.split("@,")

while True:
    passwd_input = input("\nRegex: ")

    for passwd in passwd_list:
        if re.match(f"{passwd_input}$", passwd, flags=re.I):
            print(passwd)