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
                color: #003b73;
                text-align: center;
                }

                .link {
                fill: none;
                stroke: #404040;
                stroke-width: 1.5px;
                }
                </style>

                <script type="text/javascript">

                var current = null;

                var nodesGraph = JSON.parse("{{nodes |escapejs}}");                
                var links= JSON.parse("{{links |escapejs}}");

                links.forEach(function(link) {
                    link.source = nodesGraph[link.source];
                    link.target = nodesGraph[link.target];
                });

                var force = d3.layout.force() //kreiranje force layout-a
                    .size([2000, 1000]) //raspoloziv prostor za iscrtavanje
                    .nodes(d3.values(nodesGraph)) //dodaj nodove
                    .links(links) //dodaj linkove
                    .on("tick", tick) //sta treba da se desi kada su izracunate nove pozicija elemenata
                    .linkDistance(600) //razmak izmedju elemenata
                    .charge(-550)//koliko da se elementi odbijaju
                    .gravity(0.5)
                    .start(); //pokreni izracunavanje pozicija

                var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                                        svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                                })).append('g');

                // add the links
                var link = svg.selectAll('.link')
                    .data(links)
                    .enter().append('line')
                    .attr('class', 'link');

                // add the nodes
                var node = svg.selectAll('.node')
                    .data(force.nodes()) //add
                    .enter().append('g')
                    .attr('class', 'node')
                    .attr('id', function(d){return d.id;})
                    .on('click',function(){
                    nodeClick(this);
                    });
                d3.selectAll('.node').each(function(d){nodeView(d, '#003B73');});

                function nodeView(d, color){
                    var width=30;
                    var textSize=12;

                    //Ubacivanje kruga
                    d3.select("g#"+d.id).append('circle').
                    attr('cx',0).attr('cy', 0).attr('r', width).attr('fill', color);
                    //Ubacivanje naziva prodavnice ili artikla
                    d3.select("g#"+d.id).append('text').attr('x', 0).attr('y', 4)
                    .attr('text-anchor','middle')
                    .attr('font-size',textSize).attr('font-family','poppins')
                    .attr('fill','white').text(d.id);
                }

                function tick(e) {

                    node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
                        .call(force.drag);

                    link.attr('x1', function(d) { return d.source.x; })
                        .attr('y1', function(d) { return d.source.y; })
                        .attr('x2', function(d) { return d.target.x; })
                        .attr('y2', function(d) { return d.target.y; });

                }
                

                </script>
                """

        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        print(nodes)
        print(links)
        view_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return view_html