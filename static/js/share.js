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
        },
        selected_version() {
            return this.selected.version;
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
        changePage: function(page) {
            this.page = page;
        },
        openShareModal: function(repository) {
            var self = this;
            this.resetSelection();
            this.selected.repository = repository;
            repository.share_loading = true;
            axios.get('https://api.github.com/repos/'+repository.full_name+'/tags')
                .then(function (versions) {
                    self.selected.versions = versions.data;
                    $('.ui.modal').modal('show');
                    $('.ui.dropdown').dropdown();
                    repository.share_loading = false;
                });
        },
        resetSelection: function() {
            this.selected = {
                repository: {},
                versions: [],
                entrypoints: [],
                version: false,
                entrypoint: false
            };
        },
        share: function(repository) {
            var self = this;
            repository.share_loading = true;
            axios.post('/share/' + repository.name, {
                version: this.selected.version,
                entrypoint: this.selected.entrypoint
            }).then(function(response) {
                repository.share_loading = false;
                if (response.data.success) {
                    repository.is_shared = true;
                    repository.shared_version = self.selected.version;
                    $.uiAlert({
                        textHead: 'Adding done !',
                        text: 'Your package has been added on public catalog',
                        bgcolor: '#19c3aa',
                        textcolor: '#fff',
                        position: 'top-right',
                        icon: 'warning sign',
                        time: 3,
                    });
                } else {
                    $.uiAlert({
                        textHead: 'Oups !',
                        text: 'An error occured during the operation',
                        bgcolor: '#f2711c',
                        textcolor: '#fff',
                        position: 'top-right',
                        icon: 'checkmark box',
                        time: 3,
                    });
                }
            });
        },
        update: function(repository) {
            var self = this;
            repository.share_loading = true;
            axios.post('/share_update/' + repository.name, {
                version: this.selected.version,
                entrypoint: this.selected.entrypoint
            }).then(function(response) {
                repository.share_loading = false;
                if (response.data.success) {
                    repository.shared_version = self.selected.version;
                    $.uiAlert({
                        textHead: 'Update done !',
                        text: 'Your package has been updated from public catalog',
                        bgcolor: '#19c3aa',
                        textcolor: '#fff',
                        position: 'top-right',
                        icon: 'warning sign',
                        time: 3,
                    });
                } else {
                    $.uiAlert({
                        textHead: 'Oups !',
                        text: 'An error occured during the operation',
                        bgcolor: '#f2711c',
                        textcolor: '#fff',
                        position: 'top-right',
                        icon: 'checkmark box',
                        time: 3,
                    });
                }
            });
        },
        unshare: function(repository) {
            var self = this;
            if (confirm('Are you sure your want to remove package "'+repository.name+'" from public catalog ?')) {
                repository.unshare_loading = true;
                axios.get('/unshare/' + repository.name).then(function(response) {
                    repository.unshare_loading = false;
                    if (response.data.success) {
                        repository.is_shared = false;
                        $.uiAlert({
                            textHead: 'Unsharing done !',
                            text: 'Your package has been unpublished from public catalog',
                            bgcolor: '#19c3aa',
                            textcolor: '#fff',
                            position: 'top-right',
                            icon: 'warning sign',
                            time: 3,
                        });
                    } else {
                        $.uiAlert({
                            textHead: 'Oups !',
                            text: 'An error occured during the operation',
                            bgcolor: '#f2711c',
                            textcolor: '#fff',
                            position: 'top-right',
                            icon: 'checkmark box',
                            time: 3,
                        });
                    }
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
        },
        selected_version: function(version) {
            var self = this;
            axios.get('https://api.github.com/repos/'+this.selected.repository.full_name+'/contents')
                .then(function(entrypoints) {
                    self.selected.entrypoints = entrypoints.data;
                });
        }
    }
})
