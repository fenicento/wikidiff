var n = dat.length, // number of layers
xStackMax = longest, cautionPadding = longest/3, rectpad = 8, padheight = 30, hpadding=10;

var format = d3.time.format("%Y-%m-%d");

var margin = {
	top : 40,
	right : 10,
	bottom : 20,
	left : 10
}, width = 1200 - margin.left - margin.right, height = dat.length * 40 + days*1.1 - margin.top - margin.bottom;

var y2 = d3.scale.ordinal().domain(d3.range(n)).rangeRoundBands([2, height], .08);

var x = d3.scale.linear().domain([0, xStackMax + cautionPadding]).range([5, width]);

var y = d3.time.scale().domain([getDate(oldest), getDate(newest)]).rangeRound([0, height - 20]);

var svg = d3.select("#graph").append("svg").attr("width", width + margin.left + margin.right+200).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// .on("click", function(d){
// layer.selectAll("rect")
// .style("stroke","#ddd")
// .attr("opacity",1.0);
// });

var layer = svg.selectAll(".layer").data(dat).enter().append("g").attr("class", "layer");

var rect = layer.selectAll("rect").data(function(d) {
	return d;
}).enter();

var myrects = rect.append("rect")
.attr("rx", 4)
.attr("ry", 4)
.style("fill", '#fff')
.style("stroke", function(s){if((s.change && s.change>0) || s.new) return '#F7D1B4'; else if(s.change && s.change<0) return '#9CD3F7'; else return'#ddd'})
.style("stroke-width",2)
.attr("y", function(d) {
	return y2(d.y);
})
.attr("x", function(d) {
	return x(d.start) + rectpad * d.ind+70;
})
.attr("height", padheight).attr("width", function(d) {
	return x(d.offset);
})
.attr("opacity", 1.0)
.on("click", function(d) {
	console.log(d);
	layer.selectAll("rect")
	.attr("opacity",1)
	.filter(function(f) {
		return f.tocName != d.tocName
})
.attr("opacity", 0.5);

});

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

d3.select("svg").attr("height",prev+(padheight+hpadding)*3);

var text = layer.selectAll(".label")
.data(function(d) {
	return d;
})
.enter()
.append("text").attr("x", function(d) {
	return x(d.start) +70+ rectpad * d.ind + x(d.offset) / 2
})
.attr("y", function(d) {
	return d.h + padheight / 2
})
.attr("text-anchor", "middle")
.attr("font-size", 9)
.attr('fill', '#666')
.attr("dy", ".35em")
.text(function(d) {
	if (x(d.offset) < 10)
		return "";
	else if (x(d.offset) > d.tocName.length * 7)
		return d.num + " " + d.tocName;
	else
		return d.num;
});

function getDate(d) {
	return new Date(format.parse(d));
}

//.attr("x",function(d) {return x(d.start)+rectpad*d.ind+4})
//.attr("y",function(d) {return y(d.y)+15})
