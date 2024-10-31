// static/js/app.js

const socket = new WebSocket('ws://' + window.location.host + '/ws/file_share/');

let connectedPeer = null;

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.action === 'peer_list') {
        updatePeerList(data.peers);
    } else if (data.action === 'connection_request') {
        handleConnectionRequest(data.peer_ip);
    } else if (data.action === 'connection_response') {
        handleConnectionResponse(data.success, data.peer_ip);
    } else if (data.action === 'file_transfer_status') {
        updateStatus(`File transfer to ${data.peer_ip}: ${data.success ? 'Success' : 'Failed'}`);
    }
};

function updatePeerList(peers) {
    const peerList = document.getElementById('peerList');
    peerList.innerHTML = '';
    peers.forEach(peer => {
        const li = document.createElement('li');
        li.classList.add('list-group-item');
        li.textContent = peer;
        li.addEventListener('click', () => connectToPeer(peer));
        peerList.appendChild(li);
    });
}

function connectToPeer(peer) {
    connectedPeer = peer;
    socket.send(JSON.stringify({
        action: 'connect_to_peer',
        peer_ip: peer
    }));
}

function handleConnectionRequest(peerIP) {
    const confirmed = confirm(`${peerIP} wants to connect. Accept?`);
    socket.send(JSON.stringify({
        action: 'connection_response',
        success: confirmed,
        peer_ip: peerIP
    }));
}

function handleConnectionResponse(success, peerIP) {
    if (success) {
        updateStatus(`Connected to ${peerIP}`);
        connectedPeer = peerIP;
    } else {
        updateStatus(`Failed to connect to ${peerIP}`);
    }
}

function updateStatus(message) {
    const status = document.getElementById('status');
    status.textContent = message;
}

document.getElementById('discoverPeers').addEventListener('click', () => {
    socket.send(JSON.stringify({
        action: 'discover_peers'
    }));
});

document.getElementById('connectToPeer').addEventListener('click', () => {
    const peerIPInput = document.getElementById('peerIPInput');
    const peerIP = peerIPInput.value.trim();
    if (peerIP) {
        socket.send(JSON.stringify({
            action: 'connect_to_peer',
            peer_ip: peerIP
        }));
    } else {
        updateStatus('Please enter a peer IP address.');
    }
});

document.getElementById('sendFile').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file && connectedPeer) {
        const reader = new FileReader();
        reader.onload = function(e) {
            socket.send(JSON.stringify({
                action: 'send_file',
                peer_ip: connectedPeer,
                file_data: e.target.result
            }));
        };
        reader.readAsDataURL(file);
    } else {
        updateStatus('Please select a file and connect to a peer first.');
    }
});

document.getElementById('fileInput').addEventListener('change', () => {
    document.getElementById('sendFile').disabled = false;
});