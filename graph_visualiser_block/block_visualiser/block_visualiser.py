import json

from django.template import engines
from services.visualiser_api import GraphVisualisation

class BlockVisualiser(GraphVisualisation):

    def identifier(self):
        return "block_visualiser"

    def name(self):
        return "Block view"

    def visualize(self, graph, request):
        nodes = []
        for n in graph.nodes:
            attributes = []
            for attribute_key in n.attributes.keys():
                attributes.append(attribute_key + ": " + str(n.attributes[attribute_key]))

            node_data = {
                "attributes": attributes,
                "weight": 1
            }
            nodes.append(node_data)

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

            var force = d3.layout.force()
                .size([4000, 2000])
                .nodes(d3.values(nodesGraph))
                .links(links)
                .on("tick", tick)
                .linkDistance(2000)  
                .charge(-1000)
                .gravity(0.1)
                .start();

            var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
            })).append('g');

            var padding = 20; 
            var alpha = 0.1;  

            // add the links
            var link = svg.selectAll('.link')
                .data(links)
                .enter().append('line')
                .attr('class', 'link');

            // add the block nodes
            var blockNode = svg.selectAll('.block')
                .data(force.nodes())
                .enter().append('g')
                .attr('class', 'block')
                .attr('id', function(d) {
                    return d.id;
                })
                .on('click', function(d) {
                    nodeClick(d);
                });

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

            function nodeClick(d) {
                for (var i = 0; i < d.attributes.length; i++) {
                    message += d.attributes[i] + "\\n";
                }
                alert(message);
            }

            function tick(e) {
                var k = 6 * e.alpha;
                force.nodes().forEach(function(o, i) {
                    o.y += k * (i & 1 ? 1 : -1);
                });

                force.nodes().forEach(function(o, i) {
                    force.nodes().forEach(function(d, j) {
                        if (i !== j) {
                            var deltaX = o.x - d.x;
                            var deltaY = o.y - d.y;
                            var distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
                            var minDistance = o.radius + d.radius + padding;

                            if (distance < minDistance) {
                                var displacementX = (minDistance - distance) * (deltaX / distance) * alpha;
                                var displacementY = (minDistance - distance) * (deltaY / distance) * alpha;
                                o.x += displacementX;
                                o.y += displacementY;
                                d.x -= displacementX;
                                d.y -= displacementY;
                            }
                        }
                    });
                });

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
