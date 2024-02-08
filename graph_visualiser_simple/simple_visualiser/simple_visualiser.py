from services.visualiser_api import GraphVisualisation

import json
from django.template import engines

from models.edge import Edge
from models.node import Node


class SimpleVisualiser(GraphVisualisation):

    def identifier(self):
        return 'simple_visualiser'

    def name(self):
        return 'Simple view'

    def visualize(self, graph, request):
        nodes = {}
        for n in graph.nodes:
            attributes = []
            for attribute_key in n.attributes.keys():
                attributes.append(attribute_key + ": " + str(n.attributes[attribute_key]))
            nodes[n.id] = {
                "id": "ID_" + str(n.id),
                "attributes": attributes,
                "weight": 1
            }

        links = []
        for e in graph.edges:
            link = {"source": e.fromNode.id, "target": e.toNode.id}
            links.append(link)

        view = """
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

                <style>
                .node {
                cursor: pointer;
                color: #5b5b5b;
                text-align: center;
                }

                .link {
                fill: none;
                stroke: #333333;
                stroke-width: 1.5px;
                }
                </style>

                <script type="text/javascript">
                
                    $(document).ready(function(){
                        init();
                    });
                    
                    var aspectRatioHeight = null;
                     var aspectRatioWidth = null;
                     var home = null;
                     var minimapDimensions = null;
                     var minimapViewer = null;
                     var minimapViewerDimensions = null;
                     var birdViewWidth = null;
                     var birdViewHeight = null;
                     var viewportDimensions = null;
                     var zoom = null;
                     var previousScale = 1;
                     var currentScale = 1;
                     var originalPrevScale = 1;
                    var firstZoom = true;
                    var originalGraphWidth = 0;
                    var originalGraphHeight = 0;

                     viewportDimensions = {
                       height: 500,
                       width: 600
                     }

                     aspectRatioHeight = 0.25;
                     aspectRatioWidth = 0.25;

                     minimapDimensions = {
                       height: viewportDimensions.height * aspectRatioHeight,
                       width: viewportDimensions.width * aspectRatioWidth
                     };

                     minimapViewerDimensions = {
                       height: minimapDimensions.height,
                       width: minimapDimensions.width
                     }

                     home = d3.select("#mainView").node();

                    var current = null;
    
                    var nodesGraph = JSON.parse("{{nodes |escapejs}}");                
                    var links= JSON.parse("{{links |escapejs}}");
    
                    links.forEach(function(link) {
                        link.source = nodesGraph[link.source];
                        link.target = nodesGraph[link.target];
                    });
    
                    var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                        const action = d3.event.type === "zoom" && d3.event?.sourceEvent?.type === "mousemove" ? "PAN": "ZOOM";
                            var scaleForZoom;
                            var scaleForBirdZoom = 1;

                        if(action==="ZOOM") {
                            currentScale = d3.event.scale;
                            // Check if the current scale is greater than the previous one
                            console.log("previous scale: " + previousScale)
                            console.log("current scale: " + currentScale)
                            if (currentScale > originalPrevScale) {
                                console.log("Zoom in");
                                scaleForZoom = 1.1;
                                scaleForBirdZoom = 0.9;
                            } else if (currentScale < originalPrevScale) {
                                console.log("Zoom out");
                                scaleForZoom = 0.9;
                                scaleForBirdZoom = 1.1;
                            }
                            currentScale = previousScale * scaleForZoom
                            originalPrevScale = d3.event.scale;
                            var newX = d3.event.translate[0] * scaleForZoom;
                            var newY = d3.event.translate[1] * scaleForZoom;
                            svg.attr("transform", " translate(" + [newX, newY] + ")" + " scale(" + currentScale + ")")
                            previousScale = currentScale;
                        } else {

                        }
                        updateBirdViewRect(d3.event, scaleForBirdZoom, newX, newY);
                    })).append('g');

                    function updateBirdViewRect(event, scaleForZoom, newX, newY) {
                        const action = d3.event.type === "zoom" && d3.event?.sourceEvent?.type === "mousemove" ? "PAN": "ZOOM";

                        if(action==="ZOOM") {
                            let main = d3.select("#mainView").html();
                            d3.select("#birdView").html(main);

                            console.log(originalGraphWidth + ", " + originalGraphHeight)

                            let birdWidth = $("#birdView")[0].clientWidth;
                            let birdHeight = $("#birdView")[0].clientHeight;

                            let graph = document.querySelector("#mainView g");

                            let graphWidth = document.querySelector("#mainView g").getBoundingClientRect().width;
                            let graphHeight = document.querySelector("#mainView g").getBoundingClientRect().height;
                            let graphTop = graph.getBoundingClientRect().top;
                            let graphLeft = graph.getBoundingClientRect().left;


                            let mainWidth = document.getElementById("top").offsetWidth;
                            let mainHeight = document.getElementById("top").offsetHeight;

                            // kada je graf manji od inicijalne velicine
                            if (originalGraphWidth > graphWidth || originalGraphHeight > graphHeight) {
                                minimapViewerDimensions.height = birdHeight;
                                minimapViewerDimensions.width = birdWidth;
                                if (graphTop >= 0) {
                                    minimapViewerDimensions.top = 0;
                                } else {
                                    minimapViewerDimensions.top = -((graphTop * minimapViewerDimensions.height) / mainHeight);
                                }
                                if (graphLeft >= 0) {
                                    minimapViewerDimensions.left = 0;
                                } else {
                                    minimapViewerDimensions.left = -((graphLeft * minimapViewerDimensions.width) / mainWidth);
                                }
                            } else {
                                // kada je graf veci ili jednak inicijalnoj velicini
                                minimapViewerDimensions.height = (birdHeight * mainHeight * 1.05) / graphHeight;
                                minimapViewerDimensions.width = (birdWidth * mainWidth * 1.05) / graphWidth;

                                minimapViewerDimensions.top = -((graphTop * minimapViewerDimensions.height) / mainHeight);
                                minimapViewerDimensions.left = -((graphLeft * minimapViewerDimensions.width) / mainWidth);
                            }

                        } else {
                            // console.log(event.translate)
                            //
                            // minimapViewerDimensions.top = -event.translate[1];
                            // minimapViewerDimensions.left = -event.translate[0];
                            //
                            // let graphWidth = d3.select("#mainView").select("g").node().getBBox().width;
                            // let graphHeight = d3.select("#mainView").select("g").node().getBBox().height;
                            //
                            // let mainWidth = document.getElementById("top").offsetWidth;
                            // let mainHeight = document.getElementById("top").offsetHeight;
                            //
                            // birdViewWidth = document.getElementById("divBird").offsetWidth
                            // birdViewHeight = document.getElementById("divBird").offsetHeight
                            //
                            // let scaleWidth = (birdViewWidth / mainWidth) / scaleForZoom;
                            // let scaleHeight = (birdViewHeight / mainHeight) / scaleForZoom;

                            // TODO
                            minimapViewerDimensions.top = minimapViewerDimensions.top + minimapViewerDimensions.height * scaleForZoom
                            minimapViewerDimensions.left = minimapViewerDimensions.left * minimapViewerDimensions.width * scaleForZoom
                            console.log("top: " + minimapViewerDimensions.top)
                            console.log("scale: " + scaleForZoom)
                        }

                        // Pomeranje pravougaonika u skladu sa pan transformacijom
                        // d3.select("#birdView").select('rect').attr("x", document.getElementsByTagName("rect")[0].x - event.transform.x / event.translate)
                        //     .attr("y", document.getElementsByTagName("rect")[0].y - event.transform.y / event.translate);
                    }

                    var force = d3.layout.force()
                        .charge(-1)
                        .linkDistance(600)
                        .size([1500, 800])
                        .nodes(d3.values(nodesGraph))
                        .links(links)
                        .on("tick", tick)
                        .gravity(0.3)
                        .start();

                    var link = svg.selectAll('.link')
                        .data(links)
                        .enter().append('line')
                        .attr('class', 'link');

                    var node = svg.selectAll('.node')
                        .data(force.nodes())
                        .enter().append('g')
                        .attr('class', 'node')
                        .attr('id', function(d){return d.id;})
                        .on('click', clicked);
                    d3.selectAll('.node').each(function(d){nodeView(d, '#595959');});

                    function nodeView(d, color){
                        var width=30;
                        var textSize=12;

                        d3.select("g#"+d.id).append('circle').
                        attr('cx',0).attr('cy', 0).attr('r', width).attr('fill', color);

                        d3.select("g#"+d.id).append('text').attr('x', 0).attr('y', 4)
                        .attr('text-anchor','middle')
                        .attr('font-size',textSize).attr('font-family','poppins')
                        .attr('fill','white').text(d.id);
                    }

                    while (force.alpha() > force.alphaMin()) { force.tick(); ticked(); }

                    function tick(e) {

                        node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                            .call(force.drag);

                        link.attr('x1', function(d) { return d.source.x; })
                            .attr('y1', function(d) { return d.source.y; })
                            .attr('x2', function(d) { return d.target.x; })
                            .attr('y2', function(d) { return d.target.y; });

                    }

                    function ticked() {
                        // console.log("Ticked");
                        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
                    }

                    function clicked(el){
                        console.log("USAO U CLICKED")
                        var message = "";
                        message += "ID:" + el.index + ", ";
                        if(current != null) {
                            //d3.selectAll('.node').each(function(d){nodeView(d, '#595959');});
                            nodeView(nodesGraph[current.index], '#1a324c')
                        }
                        var node = nodesGraph[el.index];
                        current = node;
                        nodeView(current, '#1a324c')
                        for(var i=0;i<node.attributes.length;i++) {
                            message += node.attributes[i] + ", ";
                        }
                        console.log("PORUKA: " + message)
                        alert(message)
                        const wait = (n) => new Promise((resolve) => setTimeout(resolve, n));
                        const changeBackColor = async () => {
                          await wait(5000);
                          nodeView(node, '#595959')
                          node.attr('transform', function(d) {return 'translate(' + d.x + ',' + d.y + ')';}).call(force.drag);
                        };
                        // call the async function
                        changeBackColor();
                        node.attr('transform', function(d) {return 'translate(' + d.x + ',' + d.y + ')';}).call(force.drag);
                    }

                    init();

                    function init() {
                        let main = d3.select("#mainView").node();

                        let graphWidth = d3.select("#mainView").select("g").node().getBBox().width;
                        let graphHeight = d3.select("#mainView").select("g").node().getBBox().height;

                        let mainWidth = document.getElementById("top").offsetWidth;
                        let mainHeight = document.getElementById("top").offsetHeight;

                        let scaleWidth = mainWidth / graphWidth;
                        let scaleHeight = mainHeight / graphHeight;

                        let scale = 0;
                        if(scaleWidth < scaleHeight){
                            scale = scaleWidth;
                        }else{
                            scale = scaleHeight;
                        }

                        let birdWidth = $("#birdView")[0].clientWidth;
                        let birdHeight = $("#birdView")[0].clientHeight;

                        minimapViewerDimensions.height = birdHeight;
                        minimapViewerDimensions.width = birdWidth;
                        minimapViewerDimensions.top = 0;
                        minimapViewerDimensions.left = 0;

                        let x = d3.select("#mainView").select("g").node().getBBox().x;
                        let y = d3.select("#mainView").select("g").node().getBBox().y;
                        d3.select("#mainView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");

                        previousScale = scale;

                        setTimeout(() => {
                            zoom_in_main()
                        }, 2000);

                        setTimeout(() => {
                            zoom_in_main()
                        }, 4000);

                        setTimeout(() => {
                            getGraphDimensions()
                        }, 10000);

                        let observer = new MutationObserver(observer_callback);

                        observer.observe(main, {
                            subtree: true,
                            attributes: true,
                            childList: true,
                            characterData: true
                        });

                    }

                    function getGraphDimensions() {
                        let gElement = document.querySelector("#mainView g");
                        let gWidth = gElement.getBoundingClientRect().width;
                        let gHeight = gElement.getBoundingClientRect().height;
                        originalGraphWidth = gWidth;
                        originalGraphHeight = gHeight;
                        console.log(originalGraphWidth);
                    }

                    function zoom_in_main() {
                        graphWidth = d3.select("#mainView").select("g").node().getBBox().width;
                        graphHeight = d3.select("#mainView").select("g").node().getBBox().height;

                        mainWidth = document.getElementById("top").offsetWidth;
                        mainHeight = document.getElementById("top").offsetHeight;

                        scaleWidth = mainWidth / graphWidth;
                        scaleHeight = mainHeight / graphHeight;

                        scale = 0;
                        if(scaleWidth < scaleHeight){
                            scale = scaleWidth;
                        }else{
                            scale = scaleHeight;
                        }

                        x = d3.select("#mainView").select("g").node().getBBox().x;
                        y = d3.select("#mainView").select("g").node().getBBox().y;
                        d3.select("#mainView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");

                        previousScale = scale;

                        force = force.charge(-550)
                        force.start()
                    }

                    function observer_callback() {
                        let main = d3.select("#mainView").html();
                        d3.select("#birdView").html(main);

                        let graphWidth = d3.select("#mainView").select("g").node().getBBox().width;
                        let graphHeight = d3.select("#mainView").select("g").node().getBBox().height;

                        let mainWidth = document.getElementById("top").offsetWidth;
                        let mainHeight = document.getElementById("top").offsetHeight;


                        birdViewWidth = document.getElementById("divBird").offsetWidth
                        birdViewHeight = document.getElementById("divBird").offsetHeight


                        let birdWidth = $("#birdView")[0].clientWidth;
                        let birdHeight = $("#birdView")[0].clientHeight;


                        let scaleWidth = birdWidth / graphWidth;
                        let scaleHeight = birdHeight / graphHeight;

                        let scale = 0;
                        if(scaleWidth < scaleHeight){
                            scale = scaleWidth;
                        }else{
                            scale = scaleHeight;
                        }

                        let x = d3.select("#birdView").select("g").node().getBBox().x;
                        let y = d3.select("#birdView").select("g").node().getBBox().y;
                        d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");


                        let graphPosition = null;

                        let element = document.getElementsByTagName('g')[0];

                        if (element) {
                            // Dobijanje dimenzija i pozicije elementa u odnosu na prozor pregledaca
                            let rect = element.getBoundingClientRect();

                            // Relativna pozicija u odnosu na prozor pregledaca
                            graphPosition = {
                                top: rect.top,
                                left: rect.left,
                                width: rect.width,
                                height: rect.height
                            };

                            // minimapViewerDimensions.top = graphPosition.top * birdViewHeight/mainHeight;
                            // minimapViewerDimensions.left = graphPosition.left * birdViewWidth/mainWidth;
                        }


                        let rect = d3.select("#divBird").select('rect');

                         //Add a white viewbox onto the top of the minimap
                         minimapViewer = d3.select("#birdView")
                           .append("rect")
                           .attr("fill", "transparent")
                           .attr("height", minimapViewerDimensions.height)
                           .attr("width", minimapViewerDimensions.width)
                           .attr("x", minimapViewerDimensions.left)
                           .attr("y", minimapViewerDimensions.top)
                             .attr("position", "absolute")
                           .attr("id", "minimapViewer")
                           .attr("stroke", 'red')
                           .attr("stroke-width", 2);

                    }
                </script>
                """

        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        print(nodes)
        print(links)
        view_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return view_html