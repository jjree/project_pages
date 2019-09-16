// from data.js
var tableData = data;
createTable();
var rowCount = $('#ufo-table >tbody >tr:visible').length;
document.getElementById("result-count").innerText = "Result Count: " +rowCount;


// Create Table populates table with tableData from data.js file
function createTable(){
    let t = document.querySelector("table");
    var tbody = t.querySelector("tbody"); //getElementById("data");
    var d = tableData;
    var date = document.getElementById("datetime").value;

    for(let element of d){
        let row = tbody.insertRow();
        for (key in element){
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text);
        }
    }
}

// Notifies when filter button is clicked and calls filter function with value of user input
function filterButtonClicked(){
    var values = [];
    values.push(document.getElementById("datetime").value.toLowerCase());
    values.push(document.getElementById("city").value.toLowerCase());
    values.push(document.getElementById("state").value.toLowerCase());
    values.push(document.getElementById("country").value.toLowerCase());
    values.push(document.getElementById("shape").value.toLowerCase());
    console.log(values);
    filter(values);
}

function unfilterButtonClicked(){
    var values = ["","","","",""];
    document.getElementById("datetime").value = "";
    document.getElementById("city").value = "";
    document.getElementById("state").value = "";
    document.getElementById("country").value = "";
    document.getElementById("shape").value = "";
    console.log(values);
    
    let t = document.querySelector("table");
    var tbody = t.querySelector("tbody"); 
    tr = t.getElementsByTagName("tr");

    for (var i=0; i<tr.length; i++){
        tr[i].style.display = "";
    }
    var rowCount = $('#ufo-table >tbody >tr:visible').length;
    document.getElementById("result-count").innerText = "Result Count: " +rowCount;
    }

// Filters which table rows to display to the user based on users search input
function filter(values){
    let t = document.querySelector("table");
    var tbody = t.querySelector("tbody"); 
    tr = t.getElementsByTagName("tr");

    for (var i =0; i<tr.length; i++){
        omitted = false;
        // values = document.getElementById("datetime").value
        tdate = tr[i].getElementsByTagName("td")[0];
        tcity = tr[i].getElementsByTagName("td")[1];
        tstate = tr[i].getElementsByTagName("td")[2];
        tcountry = tr[i].getElementsByTagName("td")[3];
        tshape = tr[i].getElementsByTagName("td")[4];
        // DATETIME
        if(values[0] != ""){
            if(tdate){
                tdate_text = tdate.textContext || tdate.innerText;
                if((tdate_text.toLowerCase().indexOf(values[0]) > -1) && (!omitted)){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                    omitted = true;
                }
            }
        }
        // CITY
        if(values[1] != ""){
            if(tcity){
                tcity_text = tcity.textContext || tcity.innerText;
                if((tcity_text.toLowerCase().indexOf(values[1]) > -1) && (!omitted)){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                    omitted = true;
                }
            }
        }
        // STATE
        if(values[2] != ""){
            if(tstate){
                tstate_text = tstate.textContext || tstate.innerText;
                if((tstate_text.toLowerCase().indexOf(values[2]) > -1) && (!omitted)){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                    omitted = true;
                }
            }
        }
        // COUNTRY
        if(values[3] != ""){
            if(tcountry){
                tcountry_text = tcountry.textContext || tcountry.innerText;
                if((tcountry_text.toLowerCase().indexOf(values[3]) > -1) && (!omitted)){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                    omitted = true;
                }
            }
        }
        // SHAPE
        if(values[4] != ""){
            if(tshape){
                tshape_text = tshape.textContext || tshape.innerText;
                if((tshape_text.toLowerCase().indexOf(values[4]) > -1) && (!omitted)){
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                    omitted = true;
                }
            }
        }
    }
    var rowCount = $('#ufo-table >tbody >tr:visible').length;
    document.getElementById("result-count").innerText = "Result Count: " +rowCount;
    }
