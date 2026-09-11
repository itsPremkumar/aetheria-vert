// Aetheria Graph Visualization
async function loadGraph() {
    const resp = await fetch('/graph/data');
    const data = await resp.json();
    
    const container = document.getElementById('graph-viz');
    const statsDiv = document.getElementById('graph-stats');
    
    const statsResp = await fetch('/graph/stats');
    const stats = await statsResp.json();
    statsDiv.innerHTML = `
        <p>Nodes: ${stats.total_nodes}</p>
        <p>Edges: ${stats.total_edges}</p>
        <p>Groups: ${stats.groups.join(', ')}</p>
    `;

    const width = container.clientWidth || 800;
    const height = 500;
    
    const svg = d3.select('#graph-viz')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.edges).id(d => d.id))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
        .selectAll('line')
        .data(data.edges)
        .enter()
        .append('line')
        .attr('stroke', '#999')
        .attr('stroke-width', 2);

    const node = svg.append('g')
        .selectAll('circle')
        .data(data.nodes)
        .enter()
        .append('circle')
        .attr('r', 20)
        .attr('fill', d => {
            if (d.group === 'disease') return '#ef4444';
            if (d.group === 'drug') return '#10b981';
            return '#6366f1';
        })
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    const label = svg.append('g')
        .selectAll('text')
        .data(data.nodes)
        .enter()
        .append('text')
        .text(d => d.label)
        .attr('font-size', 12)
        .attr('fill', '#eaeaea')
        .attr('text-anchor', 'middle')
        .attr('dy', 30);

    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
        label
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

document.addEventListener('DOMContentLoaded', loadGraph);
