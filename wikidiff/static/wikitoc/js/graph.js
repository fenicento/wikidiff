


var n = dat.length, // number of layers
xStackMax = longest, cautionPadding = longest/1.6, rectpad = 23, padheight = 30, hpadding=10, icowidth=50;

var format = d3.time.format("%Y-%m-%d");

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
		if((d.change>100) || d.new) 
			return 'url(#more1)';
		else if (d.change>50) 
			return 'url(#more2)';
		else if (d.change>0) 
			return 'url(#more3)';
		else return '#fff';
			
		})
	.style("stroke", function(s){if((s.change && s.change>0) || s.new) return '#F7D1B4'; else if(s.change && s.change<0) return '#9CD3F7'; else return'#ddd'})
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
}


function getDate(d) {
	return new Date(format.parse(d));
}

//.attr("x",function(d) {return x(d.start)+rectpad*d.ind+4})
//.attr("y",function(d) {return y(d.y)+15})
