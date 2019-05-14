import zlib
import os
import time
import shutil
import json

from_path = 'D:/work/client/sanguoclient_branch/banshu_ios3/sanguoclient/resource'
to_path = './output'


class TempVo():
    url = ''
    name = ''
    crc_url = ''
    crc_name = ''


def cal_crc(p_file):
    """
    计算文件的crc
    :param p_file:
    :return:
    """
    prev = 0
    for each_line in open(p_file, 'rb'):
        prev = zlib.crc32(each_line, prev)
    return '%X' % (prev & 0xffffffff)


temp_map = None


def add_to_resource_map(p_url, p_crc_url):
    global temp_map
    global resource_map
    if resource_map:  # 源映射表已经载入
        if temp_map:  # 以前有缓存的map
            # 把缓存的map转存到resource_map中
            for v in temp_map.values():
                replace_url(resource_map, v.url, v.crc_url)
            temp_map = None
        replace_url(resource_map, p_url, p_crc_url)
        pass
    else:  # 源映射表还没载入
        if not temp_map:
            temp_map = {}
        vo = TempVo()
        vo.url = p_url
        vo.crc_url = p_crc_url
        temp_map[p_url] = vo
        pass


def replace_url(p_map, p_url, p_crc_url):
    obj = p_map[p_url]
    if obj:
        obj['url'] = p_crc_url  # 替换url


if __name__ == '__main__':
    file_count = 0
    json_dict = ''
    start = time.time()
    global resource_map
    for root, dirs, files in os.walk(from_path):
        from_abs_path = os.path.abspath(from_path)
        to_abs_path = os.path.abspath(to_path)
        for file_name in files:
            source_path = os.path.abspath(os.path.join(root, file_name))
            rel_path = os.path.relpath(source_path, from_abs_path)
            target_path = os.path.join(to_abs_path, rel_path)
            file_name_without_ext, ext = os.path.splitext(file_name)  # 分解文件名的扩展名
            # print(file_name, file_name_without_ext, ext)
            if file_name == 'default.res.json':
                with open(source_path, 'r') as f:
                    json_dict = json.loads(f.read())
                    resource_list = json_dict['resources']
                    resource_map = {}
                    for obj in resource_list:
                        resource_map[obj['url']] = obj
                    res_json_path = target_path
                pass
            else:
                json_key_url = rel_path.replace("\\", '/')
                # print(json_key_url)
                # print(file_name)
                crc_value = cal_crc(source_path)
                crc_name = file_name_without_ext + '_' + str(crc_value).lower() + ext
                crc_url = json_key_url.replace(file_name, crc_name)
                # print(crc_url)
                add_to_resource_map(json_key_url, crc_url)
                parent = os.path.dirname(target_path)
                new_file_path = os.path.join(parent, file_name_without_ext + '_' + str(crc_value).lower() + ext)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                if not os.path.exists(new_file_path):
                    shutil.copyfile(source_path, new_file_path)
                file_count += 1
    if resource_map:
        result_list = []
        for v in resource_map.values():
            result_list.append(v)
        json_dict['resources'] = result_list
        json_pack = json.dumps(json_dict, ensure_ascii=False, separators=(',', ':'))
        parent = os.path.dirname(res_json_path)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(res_json_path, 'w', encoding='utf-8') as f:
            f.write(json_pack)


    # crc_value = cal_crc(from_path)
    # print(crc_value)

    print('文件总数：%s' % file_count)
    end = time.time()
    print('总用时', end - start)
