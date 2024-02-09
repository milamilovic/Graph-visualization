import json
from django.template import engines
from services.visualiser_api import GraphVisualisation

class BlockVisualiser(GraphVisualisation):

    def identifier(self):
        return "block_visualiser"

    def name(self):
        return "Block view"

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
            .block {
                cursor: pointer;
                color: #5b5b5b;
                text-align: center;
                box-sizing: border-box; 
                background-color: #5b5b5b;
                border: 2px solid #003B73;
                border-radius: 5px; 
            }

            .link {
                fill: none;
                stroke: #003B73;
                stroke-width: 1.5px;
            }
            </style>

            <script type="text/javascript">
            
            $(document).ready(function(){
                init();
            });
            
            var aspectRatioHeight = null;
             var aspectRatioWidth = null;
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

            var current = null;

            var nodesGraph = JSON.parse("{{nodes |escapejs}}");
            var links = JSON.parse("{{links |escapejs}}");

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
                    var newX1 = d3.event.translate[0] * previousScale;
                    var newY1 = d3.event.translate[1] * previousScale;
                    svg.attr("transform", " translate(" + [newX1, newY1] + ")" + " scale(" + previousScale + ")")
                }
                updateBirdViewRect(d3.event);
            })).append('g');

            function updateBirdViewRect(event) {
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
                }
            }

            var force = d3.layout.force()
                .charge(-1)
                .linkDistance(2000)
                .size([4000, 2000])
                .nodes(d3.values(nodesGraph))
                .links(links)
                .on("tick", tick)
                .gravity(0.1)
                .start();

            var link = svg.selectAll('.link')
                .data(links)
                .enter().append('line')
                .attr('class', 'link');

            var blockNode = svg.selectAll('.block')
                .data(force.nodes())
                .enter().append('g')
                .attr('class', 'block')
                .attr('id', function(d) {
                    return d.id;
                })
                .on('click', clicked);

            blockNode.each(function(d) {
                var textLength = d.attributes.join(" ").length;
                var lineHeight = 15;  
                var lines = Math.ceil(textLength / 20);  
                var width = Math.max(100, textLength * 5);  

                d3.select(this).append('rect')
                    .attr('x', -width / 2)
                    .attr('y', -lines * lineHeight / 2)  
                    .attr('width', width)
                    .attr('height', lines * lineHeight)
                    .attr('fill', '#5b5b5b')
                    .attr('stroke', '#003B73');

                d3.select(this).selectAll('text.attribute')
                    .data([d.id].concat(d.attributes))
                    .enter()
                    .append('text')
                    .attr('x', 0)
                    .attr('y', function(_, i) {
                        return -lines * lineHeight / 2 + 15 + i * lineHeight;  
                    })
                    .attr('text-anchor', 'middle')
                    .attr('font-size', 12)
                    .attr('font-family', 'poppins')
                    .attr('fill', 'white')
                    .text(function(attribute) {
                        return attribute;
                    });
            });
            
            function nodeView(d, color){
                var width=30;
                var textSize=12;

                d3.select("g#"+d.id).selectAll("rect").remove(); // Remove existing rectangles
                d3.select("g#"+d.id).selectAll("text").remove(); // Remove existing text

                var textLength = d.attributes.join(" ").length;
                var lineHeight = 15;  
                var lines = Math.ceil(textLength / 20);  
                var rectWidth = Math.max(100, textLength * 5);  

                d3.select("g#"+d.id).append('rect')
                    .attr('x', -rectWidth / 2)
                    .attr('y', -lines * lineHeight / 2)  
                    .attr('width', rectWidth)
                    .attr('height', lines * lineHeight)
                    .attr('fill', color)
                    .attr('stroke', '#003B73');

                d3.select("g#"+d.id).selectAll('text.attribute')
                    .data([d.id].concat(d.attributes))
                    .enter()
                    .append('text')
                    .attr('x', 0)
                    .attr('y', function(_, i) {
                        return -lines * lineHeight / 2 + 15 + i * lineHeight;  
                    })
                    .attr('text-anchor', 'middle')
                    .attr('font-size', 12)
                    .attr('font-family', 'poppins')
                    .attr('fill', 'white')
                    .text(function(attribute) {
                        return attribute;
                    });
            }


            function clicked(d) {
                console.log("USAO U CLICKED")
                var message = "";
                const id = d.id.replace("ID_", "");
                message += "ID:" + id + ", ";
                if(current != null) {
                    // d3.selectAll('.node').each(function(d){nodeView(d, '#595959');});
                    nodeView(nodesGraph[id], '#1a324c')
                }
                var node = nodesGraph[id];
                current = node;
                nodeView(current, '#1a324c')
                for(var i=0;i<node.attributes.length;i++) {
                    message += node.attributes[i] + ", ";
                }
                console.log("PORUKA: " + message)
                alert(message)
                
                const dynamicTreeContainer = document.getElementById('dynamic-tree');
                const xhr = new XMLHttpRequest();
                xhr.open('GET', `/${id};select`, true);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        dynamicTreeContainer.innerHTML = xhr.responseText;

                        const newToggles = dynamicTreeContainer.querySelectorAll('.node-toggle');
                        newToggles.forEach(toggle => {
                            toggle.addEventListener('click', function (event) {
                                event.preventDefault();
                                const newNode = this.parentNode;
                                toggleNode(newNode);
                            });
                        });
                        let nodesTree = document.querySelectorAll('.node-toggle');
                        nodesTree.forEach(toggle => {
                            toggle.addEventListener('click', function (event) {
                                event.preventDefault();
                                const node = this.parentNode;
                                let newSelected = node.querySelector("#object-id").innerHTML;
                                if (current != null) {
                                    nodeView(current, "#003B73")
                                }
                                current = nodesGraph[newSelected];
                                nodeView(current, "red");
                            });
                        });
                        if (document.getElementById('last-opened-node') != null) {
                            const lastOpenedNode = document.getElementById('last-opened-node').innerHTML;
                            element = document.getElementById(lastOpenedNode);
                            if (element) {
                                scrollIfNeeded(element, document.getElementById('tree'));
                                element.classList.add("selected-item");
                            }
                        }
                    }
                };
                xhr.send();

                const wait = (n) => new Promise((resolve) => setTimeout(resolve, n));
                const changeBackColor = async () => {
                    await wait(5000);
                    nodeView(d, '#595959');
                    node.attr('transform', function(d) {return 'translate(' + d.x + ',' + d.y + ')';}).call(force.drag);
                };
                changeBackColor();
                node.attr('transform', function(d) {return 'translate(' + d.x + ',' + d.y + ')';}).call(force.drag);
            }

            function tick() {
                blockNode.attr("transform", function(d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });

                link.attr('x1', function(d) {
                    return d.source.x;
                })
                .attr('y1', function(d) {
                    return d.source.y;
                })
                .attr('x2', function(d) {
                    return d.target.x;
                })
                .attr('y2', function(d) {
                    return d.target.y;
                });
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

                force = force.charge(-1000)
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
        view_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return view_html
