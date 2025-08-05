from django.utils.safestring import mark_safe

"""
    将需要分页的queryset传入
    html方法返回页码html可直接在页面中渲染
"""

class Pagination(object):
    def __init__(self, request, queryset, page_size=10, plus=5, page_gram='page'):
        """
            request: request
            queryset: 传入的是需要分页的 queryset 所以那些搜索之类的筛选条件需要自己进行筛选
            page_size: 每一页显示的数据条目数量
            plus: 页码显示当前页的前 plus 页 和 后 plus 页
            page_gram: 页码参数 默认为 'page'
        """
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_gram, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.queryset = queryset
        self.plus = plus
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size
        self.page_param = page_gram
        self.queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, self.page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
    def html(self):
        """
            返回页码的相关html
        """
        # 当数据库中的数据很少的时候
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当数据库中的数据很多的时候
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            elif self.page >= self.total_page_count - self.plus:
                start_page = self.total_page_count - 2 * self.plus
                end_page = self.total_page_count
            else:
                start_page = self.page - self.plus
                end_page = self.page + self.plus
        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append("<li><a href='?{}'>首页</a></li>".format(self.query_dict.urlencode()))

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            ele = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            ele = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(ele)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = "<li class='active'><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            else:
                ele = "<li><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            ele = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            ele = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(ele)

        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(
            "<li><a href='?{}'>尾页</a></li>".format(self.query_dict.urlencode()))
        hidden_fields = []
        for key,value in self.query_dict.items():
            if key!=self.page_param:
                hidden_fields.append("<input type='hidden' name={} value={}></input>".format(key,value))
        page_str_list.append(
            """
            <li>
                <form>
                    {}
                    <div class="input-group col-md-3">
                        <input type="text" class="form-control" placeholder="输入页码跳转..." name={} style="border-radius: 0">
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="submit">跳转</button>
                        </span>
                    </div>
                </form>
            </li>
            """.format("".join(hidden_fields),self.page_param))
        page_str_list = mark_safe("".join(page_str_list))
        return page_str_list
