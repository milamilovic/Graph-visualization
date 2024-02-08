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

            var current = null;

            var nodesGraph = JSON.parse("{{nodes |escapejs}}");
            var links = JSON.parse("{{links |escapejs}}");

            links.forEach(function(link) {
                link.source = nodesGraph[link.source];
                link.target = nodesGraph[link.target];
            });

            var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
            })).append('g');

            var force = d3.layout.force()
                .charge(-1000)
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
                message += "ID:" + d.id + ", ";
                if(current != null) {
                    // d3.selectAll('.node').each(function(d){nodeView(d, '#595959');});
                    nodeView(nodesGraph[current.id.replace("ID_", "")], '#1a324c')
                }
                var node = nodesGraph[d.id.replace("ID_", "")];
                current = node;
                nodeView(current, '#1a324c')
                for(var i=0;i<node.attributes.length;i++) {
                    message += node.attributes[i] + ", ";
                }
                console.log("PORUKA: " + message)
                alert(message)
                
                const id = d.id.replace("ID_", "");
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

            </script>
        """

        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        view_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return view_html
