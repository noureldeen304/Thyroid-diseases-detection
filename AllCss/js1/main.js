// noinspection JSUnresolvedFunction

/*
 you call files contains your script as the following at index.html :
 - css files at <link href="css/your_css_file.css" rel="stylesheet"> at the start of the page as the following in order :

    <!-- Google Web Fonts -->
    <link href="css/google-fonts.css" rel="stylesheet">

    <!-- Customized Bootstrap Stylesheet -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- custom Template Stylesheet -->
    <link href="css/style.css" rel="stylesheet">

 - js files at <script src="js/your_js_file.js"></script> at the end of the page the following in order :

    <!-- JavaScript Libraries -->
    <script src="js/jquery-3.4.1.js"></script> responsive design & bootstrap dependency
    <script src="js/bootstrap@5.0.0.bundle.min.js"></script> contains prepared css classes for use at html tages
    <script src="js/collect.js_4.34.3.js"></script> #collection is object contains diff array & object methods it can help you
    https://collect.js.org/api/first.html
    <-- You custom js files -->

    you can give your html check box form tages same names acc to disease
    and unique ids

    you can play with their as the following (DOM "Document Object Model") :
    document.createElement("div");
    document.getElementByName"name");
    document.getElementById("id");
    document.getElementById("id").innerHtml()
    document.getElementById("id").innerText()

    you can play with Browser Elements as the following (BOM "Browser Object Model") :
    window.alert()
    window.onload()

    you can debug you code using console.log() and check it at browser inspect elements .. in chrome ctrl+shift+i

    then you can do your logic by collection or object ,array you want use

    * you can create map with 2 ways :
    1- new Map([
          [key1,value1],
          [key2,value2],
       ]);
     or
     2- new Map().set(key1,value1)
       .set(key2,value2)

    map common methods map.set(key,value) map.get(key) map.delete(key) map.keys() map.values()
    - to convert map into array .. you can use Array.from(map)
    - to convert map keys into array .. you can use Array.from(map.keys())
    - to convert map values into array .. you can use Array.from(map.values())

   collection is an object contains a lot of array,object,map methods which is already implemented .. we use some of it like:
      collection.where('key',value) get the items which have this value for this key
      collection.whereNotIn('key',value) get the items which have not this value for this key
      collection.max('key') get the items which have the max value for this key
      collection.pluck('pluck') select only one key of the collection
      collection.implode('-') convert collection to string with the param as a separator
      collection.first() get the first item of the collection

      for available collection methods .. please check the link below
      https://collect.js.org/api/pluck.html
 */

let allDiseases = new Map([
    ["firstDisease",{ description: "Goiter",checkedCount: getCheckedValueCount("firstDisease")}],
    ["secondDisease",{ description: "Graves",checkedCount: getCheckedValueCount("secondDisease")}],
    ["thirdDisease",{ description: "Hashimoto's flare-up",checkedCount: getCheckedValueCount("thirdDisease")}],
    ["forthDisease",{ description: "Thyroid nodules",checkedCount: getCheckedValueCount("forthDisease")}],
    ["fifthDisease",{ description: "Thyroid cancer",checkedCount: getCheckedValueCount("fifthDisease")}],
    ["sixthDisease",{ description: "Thyroiditis",checkedCount: getCheckedValueCount("sixthDisease")}]

]);



function hideResult()
{
    document.getElementById("resultDiv").style.display = 'none';
}

function toggleResult()
{
    let currentDiseases = getCurrentDiseases();
    currentDiseases.hasResult ? showResult(currentDiseases.diseaseNames) : hideResult();
}

function showResult(diseaseNames)
{
   document.getElementById("resultDiv").style.display = 'block';
   document.getElementById("result").innerHTML = diseaseNames;
}


function getCurrentDiseases()
{
    let diseasesCollection = collect(Array.from(allDiseases.values())),
        maxCheckedCount = diseasesCollection.max('checkedCount'),
        currentDiseases = diseasesCollection.where('checkedCount',maxCheckedCount).whereNotIn('checkedCount',[0,null,undefined]),
        currentDiseasesCount = currentDiseases.count(),
        hasResult = false,
        diseaseNames;

     currentDiseasesCount === 0 ? window.alert('Please select at least one symptom') : hasResult = true;
     diseaseNames = (currentDiseasesCount === 1) ? currentDiseases.first().description : currentDiseases.pluck("description").implode("<br>");

    return {
        diseaseNames :diseaseNames,
        currentDiseasesCount: currentDiseasesCount,
        hasResult: hasResult
    }
}

function getCheckedValueCount(disease)
{
    return document.querySelectorAll(`input[name=${disease}]:checked`).length;
}

function updateCheckedValues(disease)
{
    let updatedDisease = allDiseases.get(disease);
    updatedDisease.checkedCount = getCheckedValueCount(disease);
    allDiseases.set(disease,updatedDisease);
}
