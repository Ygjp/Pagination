# Pagination
django中用于处理分页的模块，方便分页时使用，提高开发效率

## 基础用法
*eg:* <br>
*这是你的代码*<br>
```
def user_list(request):
    userinfo = models.UserInfo.objects.all()
    return render(request, "user_list.html", {"userinfo": userinfo})
```
### 1、获取需要分页的queryset( models.*.object.filter(...)/all() )
### 2、传参
### 3、调用html方法获取页码的相关html
```
def user_list(request):<br>
    # 获取需要分页的queryset
    userinfo = models.UserInfo.objects.all()
    # 传参
    page_object = Pagination(request,userinfo)
    page_string = page_object.html()
    return render(request, "user_list.html", {"queryset": page_object.queryset,"page_string":page_string})
```
Pagination中有多个参数：<br>
分别是: request, queryset, page_size=10, plus=5, page_gram='page'
       
  `request`: request<br>
  `queryset`: 传入的是需要分页的 queryset 所以那些搜索之类的筛选条件需要自己进行筛选<br>
  `page_size`: 每一页显示的数据条目数量 （默认为10）<br>
  `plus`: 页码显示当前页的前 plus 页 和 后 plus 页 （默认为5）<br>
  `page_gram`: 页码参数 （默认为 'page'）<br>

### 4、在html中处理数据
eg:<br>
表格数据
```
{% for obj in queryset %}
    {{obj.xx}}
{% endfor %}
```
分页页码(使用Bootstrap实现CSS样式)
```
<ul class="pagination">
    {{ page_string }}
</ul>
```
### 最终效果

![Snipaste_2025-08-05_19-51-51](https://github.com/user-attachments/assets/8ecccb3c-6e0a-46e8-8cac-6818af664d87)

## **ps：点击和输入页码跳转时会自动携带GET参数，无需另外处理**
        
