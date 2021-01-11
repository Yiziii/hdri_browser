# hdri_browser

生成缩略图功能目前只支持Houdini18.0和Houdini18.5

这是Houdini软件HDRI查看管理的插件.
- 蓝奏云链接:https://wws.lanzous.com/iSA6rk56elg

### windows安装

1. 安装方法下载右边Releases的压缩包,解压，并确保文件夹名字为`hdri_browser`

2. 放到houdini用户设置(默认C盘文档houdini版本里)中 `scripts/python` 里(如没有找到文件夹，创建既可)

3. 打开Houdini，在工具架上新建工具架和新工具.

4. 右键Eidt Tool创建的新工具上，在Script处输入下面代码



   ```python
   from hdri_browser_dir import hdri_browser as hdri
   reload(hdri)
   hdri.show()
   ```

#### linux下安装
- 其他步骤一样
- hdri_browser文件夹最好不要跟hdri_browser.py名字一样，否则大概率读取不到，脚本内写入相对应的文件夹
- hdri_browser.py文件内
要把`第188行` `except WindowsError:` 修改成 `except:`
- (暂不支持打开文件和文件路径)
- (父对象窗口不能一直保持:-( 知识盲区)
### 使用方法

- 选择对应节点，单击图片应用HDR

- `不选择任何节点的情况下`，双击图片创建渲染器对应的hdri节点并应用

