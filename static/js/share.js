var app = new Vue({
    el: '#app-share',
    data: {
        page: 1,
        per_page: 6,
        total_count: 0,
        items: [],
        page_loading: 0,
        unshare_loading: 0
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
        changePage: function(page) {
            this.page = page;
        },
        unshare: function(repository) {
            var self = this;
            if (confirm('Are you sure your want to remove package "'+repository.name+'" from public catalog ?')) {
                this.unshare_loading++;
                axios.get('/unshare/' + repository.name).then(function(response) {
                    self.unshare_loading--;
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
