



function hideResult()
{
    document.getElementById("resultDiv").style.display = 'none';
}

function toggleResult(diseaseNames)
{
        
    document.getElementById("resultDiv").style.display === 'none' ? hideResult() : showResult(diseaseNames);
}

function showResult(diseaseNames)
{
    document.getElementById("result").innerHTML =  diseaseNames;
    document.getElementById("resultDiv").style.display = 'block';
}

