


var n = dat.length, // number of layers
xStackMax = longest, cautionPadding = longest/1.6, rectpad = 23, padheight = 30, hpadding=10, icowidth=50;

var format = d3.time.format("%Y-%m-%d");
var smallFormat = d3.time.format("%Y-%m");

var margin = {
	top : 40,
	right : 10,
	bottom : 20,
	left : 10
}, width = 1200 - margin.left - margin.right, height = dat.length * 40 + days*1.1 - margin.top - margin.bottom;

var y2 = d3.scale.ordinal().domain(d3.range(n)).rangeRoundBands([2, height], .08);

var x = d3.scale.linear().domain([0, xStackMax + cautionPadding]).range([20, width]);

var y = d3.time.scale().domain([getDate(oldest), getDate(newest)]).rangeRound([0, height - 20]);

var svg = d3.select("#graph").append("svg").attr("width", width + margin.left + margin.right+200).attr("height", height + margin.top + margin.bottom)
.on("click",deselect)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// .on("click", function(d){
// layer.selectAll("rect")
// .style("stroke","#ddd")
// .attr("opacity",1.0);
// });

var layer = svg.selectAll(".layer").data(dat).enter().append("g").attr("class", function(d,i) {return "layer"+" "+"n_"+i});

var rect = layer.selectAll("rect").data(function(d) {
	return d;
}).enter();




var myrects = rect.append("rect")
	.attr("rx", 4)
	.attr("ry", 4)
	.style("fill", function(d){
		if((d.change>1000)) 
			return 'url(#more1)';
			//return '#F7D1B4'
		else if (d.change>500) 
			return 'url(#more2)';
			//return '#FAE2CF'
		else if (d.change>0) 
			return 'url(#more3)';
			//return '#FAEDE3'
		else if (d.change<-1000) 
			return 'url(#less1)';
			//return '#9CD3F7'
		else if (d.change<-500) 
			return 'url(#less1)';
			//return '#BEE1F7'
		else if (d.change<0) 
			return 'url(#less3)';
			//return '#D9EDFA'
		else return '#fff';
			
		})
	.style("stroke", function(s){if(s.change && s.change>0) return '#F7D1B4'; else if(s.change && s.change<0) return '#9CD3F7'; else return'#ddd'})
	.style("stroke-width",2)
	.attr("y", function(d) {
		return y2(d.y);
	})
	.attr("x", function(d) {
		d.x=x(d.start) + rectpad * d.ind+70;
		return d.x;
	})
	.attr("height", padheight)
	.attr("width", function(d) {
		return x(d.offset);
	})
	.attr("opacity", 1.0)
	.on("click", highlightSel);
	



timeSpacing();

function timeSpacing() {
	prev=0
	curr=0
	layer.selectAll("g").forEach(function(d, i, arr) {
						
		myrects.filter(function(f) {
			
			return f.y == d.parentNode.__data__[0].y;
		})
		.attr('y', function(s) {
			h=prev+s.days
			s.h=h
			curr=h+padheight+hpadding
			return h
		});
		prev=curr
		
		d3.select("svg").append('text')
			.attr("class","date")
			.attr("x",0)
			.attr("y",prev+padheight/1.5)
			.text(d.parentNode.__data__[0].ts);
		
	});
}

var text = layer.selectAll(".label")
.data(function(d) {
	return d;
})
.enter()
.append("text")
.attr("x", function(d) {
	return x(d.start) +70+ rectpad * d.ind + 4
})
.attr("y", function(d) {
	return d.h +6
})

.attr("font-size", 9)
.attr('fill', '#666')
.style("background-color", "#fff")
.attr("dy", ".35em")
.text(function(d) {
	if (x(d.offset) < 40)
		return d.num;
	else if (x(d.offset) > d.tocName.length * 8)
		return d.num + " " + d.tocName;
	else
		return d.num +" "+d.tocName.substring(0,x(d.offset)/12)+"…";
});



var tips=d3.selectAll(".layer")
	.append("g")
	.attr("class","tips")

tips.each(function(d,i) {
		
		
		var news=d.filter(function(t) {
			if (t.new) return t;
		});
		
		var lasts=d.filter(function(t) {
			if (t.last) return t;
		});
		
		a=d3.select(this);
		
		news.forEach(function(r) {
		a.append("image")
        .attr("xlink:href", "/static/wikitoc/img/add.svg")
        .attr("x", r.x-3)
        .attr("y", r.h+padheight-15)
        .attr("class",function(){
        	if(r.anchor != null) return	"cl_"+r.anchor;
        	else return "cl_intro"
        })
        .attr("width", "20")
        .attr("height", "20");
		});
		
		lasts.forEach(function(r) {
		a.append("image")
		.attr("xlink:href", "/static/wikitoc/img/rem.svg")
		.attr("x",r.x+x(r.offset)-17)
		.attr("y",r.h-5)
		.attr("class",function(){
        	if(r.anchor != null) return	"cl_"+r.anchor;
        	else return "cl_intro"
        })
		.attr("width", "20")
        .attr("height", "20");
		})
	});

myrects.append("title")
.text(function(d){return d.num+" "+d.tocName;});

d3.select("svg").attr("height",prev+(padheight+hpadding)*3);



function highlightSel(d) {
	
	console.log(d);
		layer.selectAll("rect")
		.attr("opacity",1)
		.classed("bw", false)
		.filter(function(f) {
			return f.tocName != d.tocName
		})	
	.attr("opacity", 0.5)
	.attr("class","bw");
	
	text.style("fill","#444")
	.filter(function(f) {
			return f.tocName != d.tocName
		})
	.style("fill","#ddd");
	
	tips.selectAll("image").attr("opacity",0).filter(function(f){
		return d3.select(this).classed("cl_"+d.anchor);
	}).attr("opacity",1);
	
	//console.log(layer);
	myrects.filter(function(r){
		return r.tocName==d.tocName
	})
	.select(function(){return this.parentNode;})
	.transition() 
    .duration(500) 
    .attr("transform", function(s) { return "translate(" + (d.x-s.x) +"," + 0 + ")"; }); 
	d3.event.stopPropagation();
	$("#ppp").remove();
	$("#graph").after('<div id="ppp" style="top:'+(d.h+padheight*2)+'; left:'+(d.x+x(d.offset)-13)+'""><h3>'+d.num+" "+d.tocName+'</h3><p><b>Rev ID: </b>'+ d.revId+'</p><p><b>Date: </b>'+ d.ts+'</p><p><a href="http://'+lang+'.wikipedia.org/w/index.php?title='+voice+'&oldid='+d.revId+'#'+d.anchor+'">Go to wikipedia page</a></p></div>')															
}

function deselect() {
	
	layer
	.transition() 
    .duration(500)
    .attr("transform", function(s) { return "translate(" + 0 +"," + 0 + ")"; });
	
	layer.selectAll("rect")
		.attr("opacity",1)
		.classed("bw", false);
		
	text.style("fill","#444");
	
	tips.selectAll("image").attr("opacity",1);
	
	$("#ppp").remove();
}

function seqOrder() {
	
	myrects
	.transition() 
    .duration(500)
    .attr("y",function(d) {
    	return d.y*(padheight+hpadding);
    });
    
    text
    .transition() 
    .duration(500)
    .attr("y",function(d) {
    	return d.y*(padheight+hpadding)+7;
    });
    
    tips
    //.selectAll("image")
    .transition() 
    .duration(500)
    .attr("transform", function(d){
    	a=d3.select(d[0]);
    	return "translate(" + 0 + "," + ((a[0][0].y)*(padheight+hpadding)-a[0][0].h) + ")"
    	});
    
    var newH=-1;
    
    d3.selectAll(".date")
    .transition()
    .duration(500)
    .attr("y", function(d){
    	newH++;
    	return newH*(padheight+hpadding)+60;
    })
	
}


function drawTimeline() {
	
	window.tl={};
	var latl="00";
	var ofst=0;
	
	layer.selectAll("g").forEach(function(d, i, arr) {
		
		
		
		ob= d.parentNode.childNodes[0].getBoundingClientRect();
		tp=ob.top;
		bottom=ob.bottom;
						
		cur=d.parentNode.__data__[0];
		curtl=cur.ts.substr(0,7);
		curmo=cur.ts.substr(5,2);
		curyr=cur.ts.substr(0,4);
		curday=cur.ts.substr(8,2);
		
		if(latl==curtl) {
			
			tl[curyr][curmo].bottom=bottom;
			tl[curyr][curmo].bpad=30-curday;
			tl[curyr][curmo].els++;
		}	
		else {
			
			
			//tl[curyr]="";
			if(tl[curyr]==null) tl[curyr]={};
			tl[curyr][curmo]={};
			tl[curyr][curmo].els=1;
			tl[curyr][curmo].tpad=parseInt(curday,10);
			tl[curyr][curmo].bpad=30-curday;
			tl[curyr][curmo].tp=tp;
			tl[curyr][curmo].bottom=bottom;
			if(latl!="00") monthDelta(latl,curyr,curmo);
			
		}
		latl=curtl;
	});
	
	
	obToAr(tl,"years",true);
	
	
	for(var x = 0; x<tl.years.length; x++) {
		
		obToAr(tl.years[x],"months",false);
		
	}
	
	
	var timeline = svg.selectAll(".timeline")
	.data(tl.years)
	.enter()
	.append("rect")
	.attr("class","timeline")
	.attr("x", 0)
	.attr("y", function(d) {return d.months[d.months.length-1].tp-d.months[d.months.length-1].tpad-109})
	.attr("width", 30)
	.attr("height", function(d) {return d.months[0].bottom-d.months[d.months.length-1].tp})
	.style("stroke", "#ddd")
	.style("fill", "#eee");
	
	timeline[0].forEach(function(e,i,ar) {
		
		console.log(d3.select(e).datum(),i);
		
	});

}

//delirio
function monthDelta(latl, y,m) {
	
	lay=latl.substr(0,4);
	lam=latl.substr(5,2);
	
	dm=lam-m;
	dy=lay-y;
	
	if(dm>1 || dy>1 || dy==1 && dm>-11) {
		
		ld=getSmallDate(latl);
		d=getSmallDate(y+"-"+m);
		deltad=ld.getMonth() - d.getMonth() + (12 * (ld.getFullYear() - d.getFullYear()));
		laBottom=tl[lay][lam].bottom+tl[lay][lam].bpad;
		cuTop=tl[y][m].tp-tl[y][m].tpad;
		step=(cuTop-laBottom)/deltad;
		
		
		for(var i = 0; i <deltad; i++) {
			
			ld.setMonth(ld.getMonth()-1);
			
			if(tl[ld.getFullYear()]==null) tl[ld.getFullYear()]={};
			
			tl[ld.getFullYear()][pad(ld.getMonth()+1)]={};			
			tl[ld.getFullYear()][pad(ld.getMonth()+1)].els=0;
			tl[ld.getFullYear()][pad(ld.getMonth()+1)].tpad=0;
			tl[ld.getFullYear()][pad(ld.getMonth()+1)].bpad=0;
			tl[ld.getFullYear()][pad(ld.getMonth()+1)].tp=laBottom+(i*step)+5;
			tl[ld.getFullYear()][pad(ld.getMonth()+1)].bottom=laBottom+(i*step)+step-5;
		}
	}
	
	laobj=tl[lay][lam];
	cuobj=tl[y][m];
	
}

function getDate(d) {
	return new Date(format.parse(d));
}

function getSmallDate(d) {
	return new Date(smallFormat.parse(d));
}

function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

function obToAr(o,name,years) {
	
	arr=[];
	ids=[];

	for (var i in o) {
		if(i!="id"){
    	arr.push(o[i]);
    	ids.push(i);
    	//o[i].id=i;
    	delete o[i];
    }
  }
  
	

  for(var x=0; x<arr.length; x++) {
  	
  	arr[x].id=ids[x];
 	if (years) {
 		
 	} 	
  }
  
  arr.sort(function(a,b) {
		
		if (a.id>b.id) return 1;
		else if (a.id<b.id) return -1;
		else return 0;
		
	});
  
  o[name]=arr;
}

$("svg").prepend($("defs")[0]);

//.attr("x",function(d) {return x(d.start)+rectpad*d.ind+4})
//.attr("y",function(d) {return y(d.y)+15})
