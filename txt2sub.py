#!/usr/bin/python
# -*- coding: utf8 -*-
 
"""
entree: fichier texte de sous titres "temps_début 05:00 \n texte"
sortie fichier format srt

"""

debut_xml="""<?xml version="1.0"?>
<!-- <!DOCTYPE Chapters SYSTEM "matroskachapters.dtd"> -->
<Chapters>
  <EditionEntry>
"""

fin_xml="""
  </EditionEntry>
</Chapters>
"""

import os , sys, re
# import shutil
# from stat import *
# from glob import * 

fichier="sub.txt"
nom_fichier_xml="soustitre.srt"

DUREE_SUB_DEFAULT=3

def lecture_fichier(fichier):
    new_line=[]
    with open(fichier) as f:
        for line in f :
            # print(line)
            new_line.append(line)
    return new_line

def sauve_fichier( lignes,nom_fichier):
    with open( nom_fichier, "w") as f :
        
        for line in lignes :
            print( line, file=f)
    f.close()

#def extraction_info( lignes ,format=r'(.*)\s((\d)*(:\d{2})+)'):
def extraction_info( lignes ,format=r'(\d*:\d*:*\d*)(.*)'):  # ex: "10:00 ..."" ou "1:00:00 ..."
    _titre = []
    _temps = []
    for line in lignes :
        try :
            # format=r'.*(\d*:\d*)(.*)'
            format=r'\s*(\d*:\d*:*\d*)(.*)'
            # m = re.match(r'(.*)\s((\d)*(:\d{2})+)',line)
            m = re.match(format,line)
            print("titre="+m[2]+" time="+m[1])
            _titre.append(m[2])
            _temps.append(m[1])

        except :
            print(" erreur :"+line)

    return (_titre, _temps)

def enleveSautLigne(lignes):
    """
        enleve saut de ligne ex: "00:10\n text" ---> "00:10  text"
    """
    
    format=r'(\d*:\d*:*\d*)(.*)\n'  # ex: "10:00 ..."" ou "1:00:00 ..."
    
    newLignes=[]
    
    txt=" ".join(lignes)
    txt_nettoye=""
    
    Precedant_isDigit=False
    for car in txt: #recherche les \n précédés immédiatement par un chiffre => enlève le \n
        if car=='\n' :
            #debug print("NL",Precedant_isDigit)
            if Precedant_isDigit :
                car=''
        if car>= '0' and car <='9':
            Precedant_isDigit=True
        else:
            Precedant_isDigit=False
        txt_nettoye+=car
    
    # newLignes.append(txt_nettoye.split("\n"))
    newLignes=txt_nettoye.split("\n")
    
    # for line in lignes:
    #     print(line)
    #     newLignes.append(line)
    return newLignes

def creation_srt(titre,temps):
    srt=[]
    cpt=1
    for un_titre, un_temps in zip( titre,temps) :
        un_titre=un_titre.strip()
        cut=un_temps.split(":")
        hdebut=0
        mdebut=0
        sdebut=0
        if len(cut)==2 :
            mdebut=int(cut[0])
            sdebut=int(cut[1])
        elif len(cut)==3:
            hdebut=int(cut[0])
            mdebut=int(cut[1])
            sdebut=int(cut[2])
        
        sfin=sdebut+DUREE_SUB_DEFAULT #TODO augmenter les durées dynamiquement
        mfin=mdebut
        hfin=hdebut
        
        if sfin>60:
            sfin-=60
            mfin+=1
            
        if mfin>60:
            mfin-=60
            hfin+=1
        # if hdebut :
        text=f"{hdebut:02}:{mdebut:02}:{sdebut:02},000"
        # else:
        #     text=f"{mdebut:02}:{sdebut:02},000"
            
        # if hfin :
        text+=f" --> {hfin:02}:{mfin:02}:{sfin:02},000\n"
        # else :
        #     text+=f" --> {mfin:02}:{sfin:02},000\n"
            
        text+=un_titre+"\n"
         
        srt.append(f"{cpt}")   
        srt.append(text)
        srt.append("\n")
        cpt+=1
        
    return srt
        
# def creation_xml(titre,temps) :
#     xml=[]

#     xml.append(debut_xml)
#     for un_titre, un_temps in zip( titre,temps)     :
#         xml.append("<ChapterAtom>")
        
#         xml.append(f"\t<ChapterTimeStart>{un_temps}</ChapterTimeStart>")
#         xml.append("\t<ChapterDisplay>")
#         xml.append(f"\t<ChapterString>{un_titre} ({un_temps})</ChapterString>")


#         xml.append(f"\t<ChapLanguageIETF>fr</ChapLanguageIETF>")
#         xml.append(f"\t<ChapterLanguage>fre</ChapterLanguage>")

#         xml.append("\t</ChapterDisplay>")
#         xml.append("</ChapterAtom>")
#         xml.append("\n")

#     xml.append(fin_xml)

#     return xml

if __name__ == "__main__":

    try : 
        fichier = sys.argv[1]
        if fichier =='-h' :
            print("transforme un fichier texte de chapitrage vidéo en fichier xml compatible avec le format mkv")
            sys.exit()
        elif fichier[0] =="-" :
            sys.exit()

        option = sys.argv[2]
        
        out = sys.argv[3]
        if option == '-o' :
            nom_fichier_xml = out


    except SystemExit:
        print("usage txt2sub nom_fichier.txt -o nom_fichier_sortie.srt  (default sub.txt soustitre.srt")
        sys.exit()



    except :
        pass
    
    print(fichier,nom_fichier_xml)

    lignes = lecture_fichier(fichier)
    lignes = enleveSautLigne(lignes)
    
    print(lignes)#debug
    
    titre, temps = extraction_info(lignes)

    

    if len(titre)==0 : # inversion format temps titre
        print("----------------  essaie format temps titre-----------")
        temps, titre = extraction_info(lignes,format=r'((\d)*(:\d{2})+)(.*)$')
        #temps, titre = extraction_info(lignes,format=r'(\d*:\d*:*\d*)(.*)')  # ex: "10:00 ..."" ou "1:00:00 ...""
    
    print(temps)

    # xml = creation_xml(titre,temps)

    # sauve_fichier( xml,nom_fichier_xml)
    
    
    srt = creation_srt(titre,temps)
    sauve_fichier( srt,nom_fichier_xml)
    
    print("debug\n",srt)
