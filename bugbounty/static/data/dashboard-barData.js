var list_vul = JSON.parse(vul)
var list_theme={}
list_theme [list_vul[0].fields.theme]= [0,0,0]
for (var i=0; i < list_vul.length; i++){
    l= Object.keys(list_theme)
    if (!(l.includes(list_vul[i].fields.theme))){
        list_theme [list_vul[i].fields.theme]= [0,0,0];
    }

    if (list_vul[i].fields.criticality=='M'){
        list_theme [list_vul[i].fields.theme][1]++ ;

    }
    else if (list_vul[i].fields.criticality=='H'){
        list_theme [list_vul[i].fields.theme][0]++ ;
    }
    else    {
        list_theme [list_vul[i].fields.theme][2]++ ;
    }
}


function myFunction(ind) {
   var list =[]
   for(var valeur in list_theme){
     list.push(list_theme[valeur][ind] );
   }

  return   list
}
function nbvul() {
   var list =[0,0,0]
   for(var valeur in list_theme){
     list[0]= list[0] + list_theme[valeur][0]
     list[1] =list[1] + list_theme[valeur][1]
     list[2] =list[2] + list_theme[valeur][2]
   }

  return   list
}

var barData = {
	labels: Object.keys(list_theme),
	datasets: [{
		label: 'Majeures',
		backgroundColor: red,
		data: myFunction(0)
	}, {
		label: 'Modérées',
		backgroundColor: orange,
		data: myFunction(1)
	}, {
		label: 'Mineures',
		backgroundColor: yellow,
		data:  myFunction(2)
	}]
};

var pieData = {
	datasets: [{
		data: nbvul(),
		backgroundColor : [red, orange, yellow]
	}],
// These labels appear in the legend and in the tooltips when hovering different arcs
labels: ['Majeures', 'Modérées', 'Mineures']
};

        //'Infrastructures et réseau',
		//'Sécurisation des plateformes',
		//'Authentification et chiffrement',
		//'Gestion des sessions',
		//'Contrôle des autorisations',
		//'Traitement des paramètres',
		//'Conformité légale'