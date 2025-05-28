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