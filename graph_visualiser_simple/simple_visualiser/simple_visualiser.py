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

                    var current = null;
    
                    var nodesGraph = JSON.parse("{{nodes |escapejs}}");                
                    var links= JSON.parse("{{links |escapejs}}");
    
                    links.forEach(function(link) {
                        link.source = nodesGraph[link.source];
                        link.target = nodesGraph[link.target];
                    });
    
                    var svg = d3.select('#mainView').call(d3.behavior.zoom().on("zoom", function () {
                                            svg.attr("transform", " translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                                    })).append('g');
    
                    var force = d3.layout.force()
                        .charge(-550)
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
                        message += "ID:" + el.id + ", ";
                        if(current != null) {
                            d3.selectAll('.node').each(function(d){nodeView(d, '#595959');});
                            nodeView(nodesGraph[current.id.replace("ID_", "")], '#1a324c')
                        }
                        var node = nodesGraph[el.id.replace("ID_", "")];
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
            
                        let observer = new MutationObserver(observer_callback);
            
                        observer.observe(main, {
                            subtree: true,
                            attributes: true,
                            childList: true,
                            characterData: true
                        });
                    }
            
                    function observer_callback() {
                        let main = d3.select("#mainView").html();
                        d3.select("#birdView").html(main);
            
                        let mainWidth = d3.select("#mainView").select("g").node().getBBox().width;
                        let mainHeight = d3.select("#mainView").select("g").node().getBBox().height;
            
                        let birdWidth = $("#birdView")[0].clientWidth;
                        let birdHeight = $("#birdView")[0].clientHeight;
            
                        let scaleWidth = birdWidth / mainWidth;
                        let scaleHeight = birdHeight / mainHeight;
            
                        let scale = 0;
                        if(scaleWidth < scaleHeight){
                            scale = scaleWidth;
                        }else{
                            scale = scaleHeight;
                        }
                        
                        let x = d3.select("#birdView").select("g").node().getBBox().x;
                        let y = d3.select("#birdView").select("g").node().getBBox().y;
                        d3.select("#birdView").select('g').attr("transform", "translate ("+[-x*scale, -y*scale]+") scale("+ scale +")");
                    }
                </script>
                """

        django_engine = engines['django']
        view_html = django_engine.from_string(view)
        print(nodes)
        print(links)
        view_html = view_html.render({"nodes": json.dumps(nodes), "links": json.dumps(links)}, request)
        return view_html