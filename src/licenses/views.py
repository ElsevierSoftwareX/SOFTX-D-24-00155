###############################################################################################
# OSLiFe-DiSC describes OSI approved Open Source Licenses through Features (legal terms)
# according to a unified model It allows to Discover each license and understand it, to Select
# licenses satisfying a set of features and Compare two licenses to highlight the differences.
###############################################################################################

# This file is part of OSLiFe-DiSC -
# Copyright © 2022 Sihem Ben Sassi
#
# OSLiFe-DiSC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# OSLiFe-DiSC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License, version 3 for more details.
#
# You should have received a copy of the GNU Affero General Public License,
# version 3 along with OSLiFe-DiSC. If not, see <http://www.gnu.org/licenses/>.

import xml.etree.ElementTree as et
import requests
from bs4 import BeautifulSoup as bs
from anytree import Node
from flask import Blueprint, render_template, request, flash, jsonify
from werkzeug.utils import redirect
from .connection import *
import pathlib



views = Blueprint('views', __name__)           #for the path

BASE_DIR = pathlib.Path(__file__).resolve().parent
DIR_RES = BASE_DIR / "resultat"
@views.route('/', methods=['POST','GET'])           #redirect to home page
def home():
    conn, mycursor = connection()
    req1 = "select name from open_source where type ='permessive License' "
    mycursor.execute(req1)
    res1 = mycursor.fetchall()
    conn.commit()
    req2 = "select name from open_source where type ='strong copyleft License' "
    mycursor.execute(req2)
    res2 = mycursor.fetchall()
    conn.commit()
    req3 = "select name from open_source where type ='weak copyleft License' "
    mycursor.execute(req3)
    res3 = mycursor.fetchall()
    conn.commit()
    conn.close()
    result1 = []
    result2 = []
    result3 = []
    name=[]
    for i in res1:
        result1.append(i[0].replace(".xml", ""))
        name.append(i[0].replace(".xml", ""))
    for j in res2:
        result2.append(j[0].replace(".xml", ""))
        name.append(j[0].replace(".xml", ""))
    for k in res3:
        result3.append(k[0].replace(".xml", ""))
        name.append(k[0].replace(".xml", ""))
    #racine = display_tree_without_true_none(DIR_RES / "Zero-Clause BSD (0BSD)permessive_license.xml")

    racine = display_tree_ftemplate(DIR_RES / "vtlicense.xml")

    return render_template("home.html" , result1 = result1 , result2 = result2 , result3 = result3 , racine = racine , result_name= name)

@views.route('/compare', methods=['POST','GET'])        #redirect to cmpare page
def compare():
    conn, mycursor = connection()
    req= "select name from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    result = []
    for i in res:
        result.append(i[0].replace(".xml", ""))
    return render_template("compare.html" , result_name = result )

@views.route('/questionnaire' , methods=['POST' , 'GET'])          #redirect to questionnaire page
def questionnaire():
    return render_template("questionnaire.html")

@views.route('/compare_result' , methods=['POST' , 'GET'])          #redirect to compare_result page
def compare_result():
    conn, mycursor = connection()
    req = "select name from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    name = []
    for i in res:
        name.append(i[0].replace(".xml", ""))
    intersect = []
    if request.method == "POST":
        licence1 = request.form.get("license1")
        licence2 = request.form.get("license2")
        if licence1 not in name or licence2 not in name or licence1=="" or licence2=="":
            flash("name of license is not valid!!")
            return redirect("/compare")
        else:
            ch1 = licence1+".xml"
            ch2 = licence2 + ".xml"
            conn , mycursor = connection()
            req1 = "select path from open_source where name like'%"+ch1+"%'"
            req2 = "select path from open_source where name like'%" + ch2 + "%'"
            mycursor.execute(req1)
            result1 = mycursor.fetchall()
            conn.commit()
            mycursor.execute(req2)
            result2 = mycursor.fetchall()
            conn.commit()
            conn.close()
            path1 = result1[0][0]
            p1= BASE_DIR / path1
            path2 = result2[0][0]
            p2 = BASE_DIR / path2
            racine1 = display_true_tree_without_true(p1)
            racine2 = display_true_tree_without_true(p2)
            leaves1 = []
            leaves2 = []
            for i in racine1.leaves:
                leaves1.append(i.name)
            for j in racine2.leaves:
                leaves2.append(j.name)
            for k in leaves1:
                if k in leaves2:
                    intersect.append(k)
        return render_template("compare_result.html",result_name = name ,tab=intersect,res1=licence1,res2=licence2 , racine1 = racine1 , racine2 = racine2 )

@views.route('/selection', methods=['POST','GET'])          #redirect to selection page
def selection():
    conn, mycursor = connection()
    req = "select name , path from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    result = []
    for i in res:
        score = 0
        leaves = []
        racine = display_true_tree_without_true(BASE_DIR / i[1])
        for j in racine.leaves:
            leaves.append(j.name)
        same_features = []
        for k in ['Access_source_code','Use_software','Copy_software','Modify_software']:
            if k in leaves:
                score = score + 1
                same_features.append(k)
        pr = round((score * 100) / 4, 2)
        if pr != 0:
            result.append((i[0].replace(".xml", ""), pr, score, leaves.__len__(), same_features))
    result.sort(key=lambda x: x[1], reverse=True)
    conn, mycursor = connection()
    req = "select name from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    name = []
    for i in res:
        name.append(i[0].replace(".xml", ""))
    racine = display_tree_without_true_none(DIR_RES / "Zero-Clause BSD (0BSD)permessive_license.xml")
    return render_template("selection.html", result_name = name,racine = racine, res =result)

@views.route('/select_result1', methods=['POST'])          #return licenses to javascript depend to the checked checkbox
def select_result1():
    checkboxes = request.form['javascript_data']
    ch0= checkboxes.replace('[', '')
    ch1 = ch0.replace('"',"")
    ch2 = ch1.replace(']','').split(',')
    conn,mycursor= connection()
    req = "select name , path from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    result = []
    for i in res :
            score = 0
            leaves =[]
            racine = display_true_tree_without_true(BASE_DIR / i[1])
            for j in racine.leaves:
                leaves.append(j.name)
            same_features = []
            for k in ch2 :
                if k in leaves:
                    score = score+1
                    same_features.append(k)
            pr =round( (score*100)/(ch2.__len__()),2)
            if pr != 0 :
                result.append((i[0].replace(".xml",""),pr,score,leaves.__len__(),same_features))
    result.sort(key=lambda x : x[1], reverse=True)
    return (jsonify(result))

@views.route('/search', methods=['POST','GET'])         #search for a license and call display(name_license) to display the features
def search():
    if request.method == "POST":
        licence = request.form.get('search')
        conn, mycursor = connection()
        req = "select name from open_source"
        mycursor.execute(req)
        res = mycursor.fetchall()
        conn.commit()
        conn.close()
        names = []
        for i in res:
            names.append(i[0].replace(".xml", ""))
        if licence == "" or licence not in names:
            flash("No such license!!!")
            return redirect("/")
        else:
            return (display(licence))

@views.route('/display_xml', methods=['POST','GET'])         #display the xml file of the license
def display_xml():
    global res
    global names
    global license_name
    if request.method == "POST":
        ch = request.form['js_data']
        license_name = ch.replace('"', "")
        conn, mycursor = connection()
        req = "select name from open_source"
        mycursor.execute(req)
        result = mycursor.fetchall()
        conn.commit()
        conn.close()
        names = []
        for i in result:
            names.append(i[0].replace(".xml", ""))
        if license_name == "" or license_name not in names:
            flash("No such license!!!")
            return (jsonify("False"))
        else:
            lxml = license_name+".xml"
            filename = BASE_DIR / "ordered_result" / lxml
            file = open(filename, 'r')
            res1 = file.readlines()
            res = []
            for i in res1 :
                res.append(i.replace("None","False"))
            return (jsonify(res,license_name))
    return render_template('display_xml.html', res = res , license_name = license_name , result_name = names )

@views.route('/display')
@views.route('/display/<name_license>')             #after searching the license we display the information of license
def display(name_license):
    conn, mycursor = connection()
    req = "select name from open_source"
    mycursor.execute(req)
    res = mycursor.fetchall()
    conn.commit()
    conn.close()
    name = []
    for i in res:
        name.append(i[0].replace(".xml", ""))
    ch = name_license+".xml"
    conn , mycursor = connection()
    req = "select path from open_source where name='"+ch+"'"
    mycursor.execute(req)
    result = mycursor.fetchall()
    conn.commit()
    conn.close()
    path = result[0][0]
    p=BASE_DIR / path
    racine = display_true_tree_without_true(p)
    index = name_license.rfind('(')
    ID = name_license[index+1: ]
    IDs = ID.replace(')',"")
    url ="https://spdx.org/licenses/"+IDs+".html"
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    rev_div = soup.findAll("code")
    if rev_div==[]:
        return render_template('display.html', result_name = name,res=name_license ,racine = racine,IDs ='' ,full_name='' )
    else:
        return render_template('display.html', result_name=name, res=name_license, racine=racine, IDs=rev_div[2].text,full_name=rev_div[1].text)


def display_tree (licence):             #it display a tree with True, None in the end of each leaf
    arbre = et.parse(licence)
    root = arbre.getroot()
    racine = Node(root.tag)

    for i in root:
        if i.text == "None" or i.text == "True":
            ch1 = Node(i.tag + i.text, parent=racine)

        else:
            ch1 = Node(i.tag, parent=racine)

            for j in i:
                if j.text == "None" or j.text == "True":
                    ch2 = Node(j.tag + j.text, parent=ch1)

                else:

                    ch2 = Node(j.tag, parent=ch1)

                    for k in j:
                        if k.text == "None" or k.text == "True":
                            ch3 = Node(k.tag + k.text, parent=ch2)

                        else:
                            ch3 = Node(k.tag, parent=ch2)

                            for l in k:
                                if l.text == "None" or l.text == "True":
                                    ch4 = Node(l.tag + l.text, parent=ch3)
                                    #print("ch4= " + l.tag + l.text)
                                else:
                                    ch4 = Node(l.tag, parent=ch3)

                                    for p in l:
                                        if p.text == "None" or p.text == "True":
                                            Node(p.tag + p.text, parent=ch4)
    return (racine)

def display_tree_ftemplate (licence):             #it display a tree with True, None in the end of each leaf
    arbre = et.parse(licence)
    root = arbre.getroot()
    racine = Node(root.tag)

    for i in root:
        if i.text == "None" or i.text == "True":
            ch1 = Node(i.tag + i.text, parent=racine)

        else:
            ch1 = Node(i.tag, parent=racine)

            for j in i:
                if j.text == "None" or j.text == "True":
                    ch2 = Node(j.tag + j.text, parent=ch1)

                else:

                    ch2 = Node(j.tag, tooltiptext=str(j.attrib['tooltiptext']), parent=ch1)

                    for k in j:
                        if k.text == "None" or k.text == "True":
                            ch3 = Node(k.tag + k.text, tooltiptext=str(k.attrib['tooltiptext']), parent=ch2)

                        else:
                            ch3 = Node(k.tag, tooltiptext=str(k.attrib['tooltiptext']), parent=ch2)

                            for l in k:
                                if l.text == "None" or l.text == "True":
                                    ch4 = Node(l.tag + l.text, tooltiptext=str(l.attrib['tooltiptext']), parent=ch3)

                                else:
                                    ch4 = Node(l.tag, tooltiptext=str(l.attrib['tooltiptext']), parent=ch3)

                                    for p in l:
                                        if p.text == "None" or p.text == "True":
                                            Node(p.tag + p.text, tooltiptext=str(p.attrib['tooltiptext']), parent=ch4)
    return (racine)

def display_tree_without_true_none(licence):            #it display a tree without True, None in the end of each leaf
    racine = display_tree(licence)
    for m in range(racine.height):
        for i in racine.leaves:
            i.name = i.name.replace("True","")
            i.name = i.name.replace("None","")
    return (racine)

def display_true_tree(licence):                 #it display a tree with True in the end of each leaf
    racine = display_tree(licence)
    for m in range(racine.height):
        for i in racine.leaves:
            if "True" not in i.name:
                i.parent = None
    return (racine)

def display_true_tree_without_true(licence):        #it display a tree without True in the end of each leaf
    racine = display_true_tree(licence)
    for m in range(racine.height):
        for i in racine.leaves:
            i.name = i.name.replace("True","")
    return (racine)
