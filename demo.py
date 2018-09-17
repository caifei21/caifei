from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.chrome.options import Options
import time
import os
import yagmail
from PIL import Image  # 安装-pip3 install Pillow-PIL
import schedule  # 安装-pip3 install schedule


#无界面执行,但是隐藏界面执行的话,会对canvas偏移点的坐标定位不再准确
'''
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver=webdriver.Chrome(executable_path = r'/Applications/Python 3.7/chromedriver',chrome_options=chrome_options)  #读取谷歌浏览器的驱动器
'''


def job1():
    #获取 chrome 驱动器
    driver=webdriver.Chrome(executable_path = r'/Applications/Python 3.7/chromedriver')
    url=r'http://s.3dker.cn'  #设置网页链接
    driver.get(url)   #打开谷歌网页

    #登录
    username=driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[1]/div/div[1]/input')
    username.clear()
    username.send_keys(r'13216116777')
    password=driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[2]/div/div[1]/input')
    password.clear()
    password.send_keys(r'o9i8u7y6')
    login_button=driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[3]/div/button')
    login_button.click()
    time.sleep(2)

    #进入打印订单
    order_menu=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/ul/li[2]/div')
    order_menu.click()
    time.sleep(2)
    printOrder_menu=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[1]/ul/li[2]/ul/li[3]')
    printOrder_menu.click()
    time.sleep(2)


    #输入日期
    date=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[2]/form/div/div/div/div/div/div/div[1]/div/input')
    from_date="".join(time.strftime('%Y-%m',time.localtime(time.time())))+'-01'  #开始时间=当前年月+01
    to_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))   #结束时间=当前年月日
    complete_date=from_date+' - '+to_date   #拼接
    delte_date=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[2]/form/div/div/div/div/div/div/div[1]/div/i')
    delte_date.click()  #点击日期组件中的按键达到清空原来日期的目的
    date.send_keys(complete_date)  #输入准备好的日期

    #搜索
    search=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[2]/form/button/span')
    search.click()
    time.sleep(2)  


    #进入销售额 tab 页下
    sales=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[3]/div[1]/div/div/div/div/div[3]')
    sales.click()
    time.sleep(2)



    #鼠标行为
    chain=ActionChains(driver)
    # 通过printOrder_menu这个点已成功凑出了偏移点(而在尝试通过计算,试图从其他点来再次定位到偏移点时,却失败了)
    chain.move_to_element(printOrder_menu) #先移动到这个元素,即当前鼠标停留在该元素的坐标
    chain.move_by_offset(564,338)   #从当前的鼠标坐标开始移动到(x+564,y+338)
    chain.click().perform()
       
       
    #保存图片
    pic_path = '/Users/shining3d/Desktop/1/1' +'.png'
    driver.save_screenshot(pic_path)  #截取chrome当前屏幕
    global pic_path2   #global声明全局变量
    pic_path2= '/Users/shining3d/Desktop/1/'+to_date+'.png' 

    #canvas定位(为了获得canvas的宽高来估算即将裁图的区域大小)
    canvas=driver.find_element_by_xpath('//*[@id="chart"]/div[1]/canvas')
    # 裁图起点定位
    start=driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/a')
    #获得裁图起点的坐标
    left = start.location['x']
    top = start.location['y']
    #裁图大小(宽高度)
    elementWidth = start.location['x'] + canvas.size['width']
    elementHeight = start.location['y'] + canvas.size['height']+160  #+160是 起点与canvas的高度补差

    picture = Image.open(pic_path)  #读取从chrome截取的图片
    picture = picture.crop((left, top, elementWidth, elementHeight))  #裁取设定的区域
    picture.save(pic_path2)



    time.sleep(1)    #睡眠
    driver.quit()   #关闭浏览器

def job2():
    #发送邮件
    now_date=time.strftime('%Y.%m.%d',time.localtime(time.time()))
    title=r'每日销售额自动发送邮件('+now_date+')'  # 标题
    contents_words=time.strftime('%Y.%m',time.localtime(time.time()))+'.01~'+\
                   now_date+r' 本月至今的每日销售额,详情见附件预览'
    yag=yagmail.SMTP(user='yangyisheng@shining3d.com',password='Dhsqjia8',host='smtp.shining3d.com')   #咱们公司的邮箱 mail.shing3d.com
    contents=[contents_words,pic_path2]
    #yag.send(['caifeiteng@shining3d.com'],'定时邮件',contents,[ pic_path])  #附件的另一种写法
    yag.send(['caifeiteng@shining3d.com','yangyisheng@shining3d.com','zhaodonglai@shining3d.com','zhuyong@shining3d.com','yangfei@shining3d.com',\
              'wangqimin@shining3d.com','xuyifan@shining3d.com','guolei@shining3d.com'], title,contents)

    print(now_date+' 发送成功 ~')


schedule.every().day.at("8:30").do(job1)  #每天8.30执行  函数job1
schedule.every().day.at("8:30").do(job2)  #每天8.30执行  函数job2

while True:
    schedule.run_pending()
    time.sleep(1)
