# EgretCrcTool
Egret项目生成带crc版本号资源文件的工具
> exe文件是用pyinstaller打包成无依赖的执行文件，可以直接拷贝exe文件到任何地方执行

## 使用方法
```cmd
EgretCrcTool.exe --source xxx --output xxx
```

```yaml
参数说明：
--source Egret项目的resource目录
--output 计算crc重命名后的输出目录
```

## 工具目录说明
-- EgretCrcTool.exe  
> 已经打包好的程序执行文件，无需其他文件依赖
  
-- EgretCrcTool.py
> 编译的源文件，exe文件执行时候无需依赖，只作开源学习用途  
> 如果有python环境，则可代替exe工具，通过python命令直接执行（python 3.7）

-- README.md
> 说明文档