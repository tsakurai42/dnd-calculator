var class1 = d3.select("#class1choice")
var class1level = d3.select("#class1level")
var disp_class1 = d3.select("#class1chosen")
var class2 = d3.select("#class2choice")
var class2level = d3.select("#class2level")
var disp_class2 = d3.select("#class2chosen")
var weaponchoice = d3.select('#weaponchoice')
var weaponchosen = d3.select('#weaponchosen')
var feats = d3.select('#feats')
var featschosen = d3.select('#featschosen')
var weaponrarity = d3.select('#weaponrarity')
var weaponraritychosen = d3.select('#weaponraritychosen')
var fightingstyle = d3.select('#fightingstyle')
var fightingstylechosen = d3.select('#fightingstylechosen')
var dualwield = d3.select('#dualwield')
var dualwieldchosen = d3.select('#dualwieldchosen')

//document.getElementById("Add").addEventListener("load", errorcheck)

class1.on("change", () => {
    errorcheck();
    if (event.target.value == "Choose class") {
        disp_class1.text('')
    } else {
        disp_class1.text(` ${event.target.value} ${class1level.property('value')}`)
    }
})

class2.on("change", () => {
    errorcheck();
    if (event.target.value == "Choose class") {
        disp_class2.text('')
    } else {
        disp_class2.text(` / ${event.target.value} ${class2level.property('value')}`)
    }
})

class1level.on("change", () => {
    errorcheck();
    disp_class1.text(` ${class1.property('value')} ${event.target.value}`)
})

class2level.on("change", () => {
    errorcheck();
    if (class2.property('value') == "Choose class") {
        disp_class2.text('')
    } else {
        disp_class2.text(` / ${class2.property('value')} ${event.target.value}`)
    }
})

dualwield.on("change", () => {
    errorcheck();
    if (dualwield.property("checked")) {
        dualwieldchosen.text('Dual Wielding')
    } else {
        dualwieldchosen.text('')
    }

})

weaponchoice.on("change", () => {
    errorcheck();
    if (event.target.value == "Choose Your Weapon") {
        weaponchosen.text('')
    } else {
        weaponchosen.text(`${event.target.value}`)
    }
})
weaponrarity.on("change", () => {
    errorcheck();
    if (event.target.value > 0) {
        weaponraritychosen.text(event.target.value)
    }
})

fightingstyle.on("change", () => {
    errorcheck();
    fightingstylechosen.text(event.target.value)
})

feats.on("change", function (d) {
    errorcheck();
    var values = [];
    selected = d3.select(this) // select the select
        .selectAll("option:checked")  // select the selected values
        .each(function () { values.push(this.value) }); // for each of those, get its value
    featschosen.text(values)
})

// d3.select('button').on("click", () => {
//     d3.event.preventDefault();
//     window.location = "http://www.google.com"
// })

function errorcheck() {
    d3.select('#errorfield').text("")
    if ((weaponchoice.property('value') == "Longbow" || weaponchoice.property('value') == "Greataxe" ||
        weaponchoice.property('value') == "Greatsword" || weaponchoice.property('value') == "Warhammer" ||
        weaponchoice.property('value') == "Glaive" || weaponchoice.property('value') == "Hand Crossbow")
        && dualwield.property("checked")) {
        d3.select('#errorfield').text("Dual Wield + 2H weapon error (or Handcrossbow)");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if ((weaponchoice.property('value') == "Longbow" || weaponchoice.property('value') == "Mace" ||
        weaponchoice.property('value') == "Rapier" || weaponchoice.property('value') == "Shortsword" ||
        weaponchoice.property('value') == "Hand Crossbow")
        && fightingstyle.property('value') == "Great Weapon Fighting") {
        d3.select('#errorfield').text("GWF + 1H/Ranged error");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if ((class1.property('value') == class2.property('value')) && class1.property('value') != "Choose class") {
        d3.select('#errorfield').text("First and Second class cannot be the same");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (parseInt(class1level.property('value')) + parseInt(class2level.property('value')) > 20) {
        d3.select('#errorfield').text("Total class is greater than 20");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (class2.property('value') != "Choose class" && class2level.property('value') == '') {
        d3.select('#errorfield').text("Class must have a level");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (class1.property('value') != "Choose class" && class1level.property('value') == '') {
        d3.select('#errorfield').text("Class must have a level");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (class1.property('value') == 'Choose class') {
        d3.select('#errorfield').text("Must choose a class");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (weaponchoice.property('value') == "Choose Your Weapon") {
        d3.select('#errorfield').text("Choose a weapon");
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    if (!isError) {
        document.getElementById("Add").disabled = false;
        var isError = false;
    }
}
{/*                                 <option value="Greataxe">Greataxe (1d12)</option>
                                <option value="Greatsword">Greatsword (2d6)</option>
                                <option value="Hand Crossbow">Hand Crossbow (1d6)</option>
                                <option value="Mace">Mace (1d6)</option>
                                <option value="Rapier">Rapier (1d6)</option>
                                <option value="Shortsword">Shortsword (1d8)</option>
                                <option value="Warhammer">Warhammer-versatile (1d10)</option>
                                <option value="Longbow">Longbow (1d8)</option>
                                <option value="Glaive">Glaive (1d10)</option> */}