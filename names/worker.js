importScripts("https://d3js.org/d3-collection.v1.min.js");
importScripts("https://d3js.org/d3-dispatch.v1.min.js");
importScripts("https://d3js.org/d3-quadtree.v1.min.js");
importScripts("https://d3js.org/d3-timer.v1.min.js");
importScripts("https://d3js.org/d3-force.v1.min.js");

onmessage = function(event) {
  var nodes = event.data.nodes,
      links = event.data.links;

  var radiusScale = d3.scaleSqrt().domain([5, 2346]).range([5, 60])


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
    .stop();

  for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
    postMessage({type: "tick", progress: i / n});
    simulation.tick();
  }

  postMessage({type: "end", nodes: nodes, links: links});
};