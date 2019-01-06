var app = new Vue({
    el: '#app-explore',
    data: {
        page: 1,
        per_page: 6,
        total_count: 0,
        items: [],
        page_loading: 0
    },
    computed: {
        pages_count() {
            return Math.ceil(this.total_count / this.per_page);
        }
    },
    methods: {
        getRepositories: function(page) {
            var self = this;
            var page = page || 1;
            this.page_loading++;
            axios.get('/repos/all', {
                params: { page: self.page, per_page: self.per_page }
            }).then(function(repositories) {
                self.items = repositories.data;
                self.page_loading--;
            });
        }
    },
    mounted: function() {
        var self = this;

        this.getRepositories();

        this.page_loading++;
        axios.get('/repos/count').then(function(count) {
            self.total_count = count.data.count;
            self.page_loading--;
        });
    },
    watch: {
        page: function(page) {
            this.getRepositories(page);
        }
    }
});
