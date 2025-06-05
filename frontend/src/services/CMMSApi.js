class CMMSApi {
    constructor(api_url) {
        this.api_url = api_url;
    }

    getProtocols() {
        return this.fetch('/protocols', 'GET')
    }

    getProtocol(id) {
        return this.fetch('/protocols/' + id, 'GET')
    }

    uploadProtocols(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        return this.fetch('/upload-protocols', 'POST', formData);
    }

    async createProtocol(protocol) {
        const requestOptions = {
            method: 'POST',
            redirect: 'follow',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(protocol)
        };
        
        let response = await fetch(this.api_url + '/protocols', requestOptions);
        let json = await response.json();
        return json;
    }
    
    async fetch(endpoint, method, body = null) {
        const requestOptions = {
            method: method,
            redirect: 'follow',
            body
        };
        let response = await fetch(this.api_url + endpoint, requestOptions);
        let json = await response.json();

        return json;
    }
}

export default CMMSApi;
