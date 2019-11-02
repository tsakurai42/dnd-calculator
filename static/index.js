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
var bless = d3.select('#bless')
var blesschosen = d3.select('#blesschosen')
var sneakattackdiv = d3.select('#snackattack')
var sneakattack = d3.select('#sneak')
var adv = d3.select('#adv')
var shortrests = d3.select('#SRs')
var rounds = d3.select('#rounds')
//document.getElementById("Add").addEventListener("load", errorcheck)

traces = []

for (each_trace of all_tests) {
    new_trace_y = []
    for (i = 15; i<26;i++) {
        new_trace_y.push(each_trace[i])
    }
    new_trace = {
        x: [15,16,17,18,19,20,21,22,23,24,25],
        y: new_trace_y,
        type: 'line',
        name: each_trace['desc']
    }
    traces.push(new_trace)
}

layout = {
    height: 600,
    xaxis: {
        title: 'Target AC',
        dtick:1
    },
    yaxis: {
        title: 'Damage per Round'
    }
}

Plotly.newPlot('dprplotly', traces,layout);

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

bless.on("change", () => {
    errorcheck();
    if (bless.property("checked")) {
        blesschosen.text('Blessed')
    } else {
        blesschosen.text('')
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

feats.on("change", () => {
    errorcheck();
    var values = [];
    selected = d3.select(this) // select the select
        .selectAll("option:checked")  // select the selected values
        .each(function () { values.push(this.value) }); // for each of those, get its value
    featschosen.text(values)
})

shortrests.on('change', () => {
    errorcheck();
})

rounds.on('change', () => {
    errorcheck();
})
sneakattack.on('change', () => {
    errorcheck();
})
adv.on('change', () => {
    errorcheck();
})

// d3.select('button').on("click", () => {
//     d3.event.preventDefault();
//     window.location = "http://www.google.com"
// })

function errorcheck() {
    d3.select('#errorfield').text("");
    var error_text = "";
    if (class1.property('value') == "Rogue" || class2.property('value') == "Rogue") {
        sneakattackdiv.style('display',null)
    }
    if (class1.property('value') != "Rogue" && class2.property('value') != "Rogue") {
        sneakattackdiv.style('display','none')
    }

    // Cannot Dual Wield 2H weapons
    if ((weaponchoice.property('value') == "Longbow" || weaponchoice.property('value') == "Greataxe" ||
        weaponchoice.property('value') == "Greatsword" || weaponchoice.property('value') == "Warhammer" ||
        weaponchoice.property('value') == "Glaive" || weaponchoice.property('value') == "Hand Crossbow")
        && dualwield.property("checked")) {
        // d3.select('#errorfield').text("Dual Wield + 2H weapon error (or Handcrossbow)");
        error_text += "Dual Wield + 2H weapon error (or Handcrossbow). "
        document.getElementById("Add").disabled = true;
        var isError = true
    };
    // Cannot Great Weapon Fighting(Feat) with 1H or Ranged weapons
    if ((weaponchoice.property('value') == "Longbow" || weaponchoice.property('value') == "Mace" ||
        weaponchoice.property('value') == "Rapier" || weaponchoice.property('value') == "Shortsword" ||
        weaponchoice.property('value') == "Hand Crossbow")
        && fightingstyle.property('value') == "Great Weapon Fighting") {
        // d3.select('#errorfield').text("GWF + 1H/Ranged error");
        error_text += "GWF + 1H/Ranged error. ";
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    //  User selected the same class for multiclassing
    if ((class1.property('value') == class2.property('value')) && class1.property('value') != "Choose class") {
        // d3.select('#errorfield').text("First and Second class cannot be the same");
        error_text += "First and Second class cannot be the same. ";
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    // User multiclassed but combined levels is greater than 20
    if (parseInt(class1level.property('value')) + parseInt(class2level.property('value')) > 20) {
        // d3.select('#errorfield').text("Total class is greater than 20");
        error_text += "Total levels is greater than 20. "
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    // User multiclassed, but did not define a level for the 2nd class
    if (class2.property('value') != "Choose class" && class2level.property('value') == '') {
        // d3.select('#errorfield').text("Class must have a level");
        error_text += "Class 2 must have a level. ";
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    // User did not define a level for the 1st class
    if (class1.property('value') != "Choose class" && class1level.property('value') == '') {
        // d3.select('#errorfield').text("Class must have a level");
        error_text += "Class 1 must have a level. ";
        document.getElementById("Add").disabled = true;
        var isError = true
    }
    // User has not chosen a class at all yet!
    if (class1.property('value') == 'Choose class') {
        // d3.select('#errorfield').text("Must choose a class");
        document.getElementById("Add").disabled = true;
        error_text += "Must choose a class. ";
        var isError = true
    }
    // Need to choose a weapon
    if (weaponchoice.property('value') == "Choose Your Weapon") {
        // d3.select('#errorfield').text("Choose a weapon");
        error_text += "Must choose a weapon. "
        document.getElementById("Add").disabled = true;
        var isError = true
    }

    regexstring = /^\d*$/;

    if (!regexstring.test(class1level.property('value')) || !regexstring.test(class2level.property('value')) || !regexstring.test(rounds.property('value')) || !regexstring.test(shortrests.property('value')) || !regexstring.test(adv.property('value')) || !regexstring.test(sneakattack.property('value'))) {
        console.log('non-number in number only field')
    }

    console.log(error_text)
    if (isError) {
        d3.select('#errorfield').text(error_text);
    }
    
    if (!isError) {
        document.getElementById("Add").disabled = false;
        var isError = false;
    }
}