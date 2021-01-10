(function() {
	var width = 1200,
	height = 700;

	// 5 add div (also in css)
	var div = d3.select("#tooltipspot").append("div")	
    .attr("class", "tooltipspot")				
    .style("opacity", 0);


	// RESPONSIVE: creates svg object in html
	// https://stackoverflow.com/questions/16265123/resize-svg-when-window-is-resized-in-d3-js
	var svg = d3.select("div#chart")
	.append("div")
	//container class to make it responsive
	.classed("svg-container", true)
	.append("svg")
	// Responsive SVG needs these 2 attributes and no width and height attr.
	.attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox","0 0 " + width + " " + height)
    // Class to make it responsive.
    .classed("svg-content-responsive", true)
	.attr("height", height)
	.attr("width", width)
	.append("g")
	.attr("transform", "translate(0,0)")
	.attr("class", "legendOrdinal")

	// // ORIG: creates svg object in html
	// var svg = d3.select("#chart")
	// .append("svg")
	// .attr("height", height)
	// .attr("width", width)
	// .append("g")
	// .attr("transform", "translate(0,0)")

	// create svg defs (video 3, using imgs in d3 bubble charts)
	var defs = svg.append("svg:defs")

	// function that determines the size of the circles,
	// uses scaleSqrt because its the radius of a circle
	// .domain is the complete set of value ranges for your data, 
	// for NMAH thats number of items. the .range maps those values to a range of circle sizes
	// this is then called as a function in the radius value for the circle (attr "r") below
	// as well as the forceCollide function since that relies on radius values to avoid overlap
	var radiusScale = d3.scaleSqrt().domain([2, 2346]).range([3, 50])


	// the simulation is a collection of forces
	// about where we want our circles to go 
	// and how we want our circles to interact
	// first get them to the middle (force x and y)
	// second, don't have them collide, forceCollide

	// 3.1 createing forceX variable
	var forceXSeparate = d3.forceX(function(d) {
			if (d.border_check === 'ms') return '120'
			if (d.border_check === 'ccl') return '350'
			if (d.border_check === 'pmh') return '650'
			if (d.border_check === 'wi') return '950'
	}).strength(0.1)

	var forceXCombine = d3.forceX(width / 2).strength(0.1)

	var forceCollide = d3.forceCollide(function(d){
			return radiusScale(d.Items) + 2
		})

	var simulation = d3.forceSimulation()
		.force("x", forceXCombine)
		.force("y", d3.forceY(height / 2).strength(0.1))
		.force("collide", forceCollide)
		// .alphaDecay(.06)
		// added stop
		.stop();

	// read csv
	d3.queue()
	.defer(d3.csv, "nmah_names_d3.csv")
	.await(ready)


	function ready (error, datapoints) {
		
		// need to watch video 3 again, where this appending
		// of the img pattern is defined
		defs.selectAll(".img-pattern")
			.data(datapoints)
			.enter().append("pattern")
			.attr("class", "img-pattern")
			.attr("id", function(d) {
			return d.Name_ID.toLowerCase().replace(/ /g, "-")
			})
			.attr("height", "100%")
			.attr("width", "100%")
			.attr("patternContentUnits", "objectBoundingBox")
			.append("image")
			.attr("height", 1)
			.attr("width", 1)
			.attr("preserveAspectRatio", "none")
			.attr("xlink:href", function(d) {
				return d.Img_path
			});


		// create circles
		var circles = svg.selectAll(".name")
			// feed datapoints to circles
			.data(datapoints)
			.enter().append("circle")
			.attr("class", "artist")
			.attr("r", function(d){
				return radiusScale(d.Items)
			})
			.attr("fill", function(d){
				if (d.fill_check === 'ms') return 'grey'
				if (d.fill_check === 'ccl') return 'orange'
				if (d.fill_check === 'pmh') return 'brown'
				if (d.fill_check === 'wi') return 'purple'
				if (d.fill_check === 'img') return "url(#" + d.Name_ID.toLowerCase().replace(/ /g, "-") + ")"
			})
			// // working from video
			// .attr("fill", function(d){
			// 	return "url(#" + d.Name_ID.toLowerCase().replace(/ /g, "-") + ")"
			// })
			.attr("style", function(d){
				if (d.border_check === 'ms') return 'stroke: grey;'
				if (d.border_check === 'ccl') return 'stroke: orange;'
				if (d.border_check === 'pmh') return 'stroke: brown;'
				if (d.border_check === 'wi') return 'stroke: purple;'
			})
			.on("mouseover", function(d) {		
            div.transition()
            	.delay(0)
				// .duration(200)	
				.style("opacity", .9);
            div.html(d.Name_Display + 
                "<br />" + d.Items + " Items" + 
                "<br />" + d.Sub_Category +
                "<br /><a href='" + d.smithsonian_URL + "'>Click to Search NMAH</a>" +
                "<br /><a href='" + d.google_URL + "'>Click to Google</a>")
            // div	.html(d.Name_Display <br /> "-" + d.Sub_Category)
                // .style("left", (parseInt(d3.select(this).attr("cx")) + document.getElementById("body").offsetLeft) + "px")	
                // .style("top", (parseInt(d3.select(this).attr("cy")) + document.getElementById("body").offsetTop) + "px");		
                // .style("left", (d3.event.pageX) + "px")		
                // .style("top", (d3.event.pageY - 28) + "px");	
            })					
        	// .on("mouseout", function(d) {		
         //    div.transition()			
         //        .style("opacity", 0);	
        	// })

	// 3 creating buttons and event listeners
	// 4.2 change from the video - to stop the constant position recalculation
	// changed to alpha instead of alphatarget https://stackoverflow.com/questions/55730704/d3js-prevent-forcesimulation-from-recalculating-position-all-the-time
	d3.select("#name_button").on('click', function(){
		simulation
		.force("x",forceXSeparate)
		.alpha(0.9)
		.alphaDecay(.052)
		.restart()
		d3.selectAll('circle').style('visibility', 'visible');
	})
	// 3.2 additional details around updating force in simulation
	// additional info on alphatarget and why its necessary in operation
	d3.select("#combine").on('click', function(){
		simulation
		.force("x",forceXCombine)
		.alpha(0.9)
		.alphaDecay(.052)
		.restart()
		d3.selectAll('circle').style('visibility', 'visible');
	})

	// // ORIGINAL tick
	// // create a simulation, feed data (datapoints)
	// // everytime there is a tick, the simulation looks at the forces
	// // declared in the var simulation
	// simulation.nodes(datapoints)
	// // every time there is a tick of the clock, run the ticked function
	// 	.on('tick', ticked)

	// // generic function for simulation, often copy/pasted
	// function ticked(){
	// 	circles
	// 		.attr("cx", function(d){
	// 			return d.x
	// 		})
	// 		.attr("cy", function(d){
	// 			return d.y
	// 		})

	// }
// 4.1 New Tick that ticks faster
// https://stackoverflow.com/questions/26188266/how-to-speed-up-the-force-layout-animation-in-d3-js

	simulation.nodes(datapoints)
			.on('tick', ticked)
	function ticked(){
		var ticksPerRender = 3.5;
		requestAnimationFrame(function render() {
  			// for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
    	// 	simulation.tick();
    	// }
  // //v1
			for (var i = 0; i < ticksPerRender; i++) simulation.tick();
  // // orig
  // 			for (var i = 0; i < ticksPerRender; i++) {
  //   		simulation.tick();
  // }
  circles
			.attr("cx", function(d){
				return d.x
			})
			.attr("cy", function(d){
				return d.y
			})
  // UPDATE NODE AND LINK POSITIONS HERE

  if (simulation.alpha() > 0) {
    requestAnimationFrame(render);
  }
  else {
  	simulation.stop();
  }
});
}


//keep these
	}
})();