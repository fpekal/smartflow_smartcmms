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

    async uploadProtocols(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const requestOptions = {
            method: 'POST',
            body: formData,
            redirect: 'follow'
        };
        
        let response = await fetch(this.api_url + '/upload-protocols', requestOptions);
        let json = await response.json();
        return json;
    }
    
    async fetch(endpoint, method) {
        const requestOptions = {
            method: method,
            redirect: 'follow'
        };
        let response = await fetch(this.api_url + endpoint, requestOptions);
        let json = await response.json();

        return json;
    }
}

export default CMMSApi;
