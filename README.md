# hdri_browser

这是Houdini软件HDRI查看管理的插件.

### 安装

1. 安装方法下载右边Releases的压缩包,解压，并确保文件夹名字为`hdri_browser`

2. 放到houdini用户设置(默认C盘文档houdini版本里)中 `scripts/python` 里(如没有找到文件夹，创建既可)

3. 打开Houdini，在工具架上新建工具架和新工具.

4. 右键Eidt Tool创建的新工具上，在Script处输入下面代码

   ```python
   from hdri_browser import hdri_browser as hdri
   reload(hdri)
   hdri.show()
   ```





### 使用方法

- 选择对应节点，单击图片应用HDR

- `不选择任何节点的情况下`，双击图片创建渲染器对应的hdri节点并应用

