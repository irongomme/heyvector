var app = new Vue({
    el: '#app-share',
    data: {
        page: 1,
        per_page: 6,
        total_count: 0,
        items: [],
        page_loading: 0,
        selected: {
            repository: {},
            versions: [],
            entrypoints: [],
            version: false,
            entrypoint: false
        }
    },
    computed: {
        pages_count() {
            return Math.ceil(this.total_count / this.per_page);
        }
    },
    methods: {
        getUser: function() {
            var self = this;
            return axios.get('/github/user').then(function(user) {
                self.total_count = user.data.public_repos;
            });
        },
        getRepositories: function(page) {
            var self = this;
            var page = page || 1;
            this.page_loading++;
            return axios.get('/repos/user_all', {
                params: { page: self.page, per_page: self.per_page }
            }).then(function(repositories) {
                self.items = repositories.data;
                self.page_loading--;
            });
        },
        getRepositoryVersions: function(repository) {
            return axios.get('https://api.github.com/repos/'+repository.full_name+'/tags');
        },
        getRepositoryEntrypoints: function(repository) {
            return axios.get('https://api.github.com/repos/'+repository.full_name+'/contents');
        },
        changePage: function(page) {
            this.page = page;
        },
        openShareModal: function(repository) {
            var self = this;
            this.selected.repository = repository;
            repository.share_loading = true;
            axios.all([this.getRepositoryVersions(repository), this.getRepositoryEntrypoints(repository)])
                .then(axios.spread(function (versions, entrypoints) {
                    self.selected.versions = versions.data;
                    self.selected.entrypoints = entrypoints.data;
                    $('.ui.modal').modal('show');
                    $('.ui.dropdown').dropdown();
                    repository.share_loading = false;
                }));
        },
        share: function(repository) {
            var self = this;
            repository.share_loading = true;
            axios.post('/share/' + repository.name, {
                version: this.selected.version,
                entrypoint: this.selected.entrypoint
            }).then(function(response) {
                repository.share_loading = false;
                repository.is_shared = true;
            });
        },
        unshare: function(repository) {
            var self = this;
            if (confirm('Are you sure your want to remove package "'+repository.name+'" from public catalog ?')) {
                repository.unshare_loading = true;
                axios.get('/unshare/' + repository.name).then(function(response) {
                    repository.unshare_loading = false;
                    repository.is_shared = false;
                });
            }
        }
    },
    mounted: function() {
        axios.all([this.getUser(), this.getRepositories()]);
    },
    watch: {
        page: function(page) {
            this.getRepositories(page);
        }
    }
})
