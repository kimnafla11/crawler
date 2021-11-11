from matplotlib import font_manager, rc

import matplotlib
import matplotlib.pyplot as plt

font_location ='C:\\Users\\kimna\\AppData\\Local\\Microsoft\\Windows\\Fonts\\KoPubWorld Dotum Medium.ttf'
#'C:\Users\kimna\AppData\Local\Microsoft\Windows\Fonts\KoPubWorld Dotum Medium.ttf'
font_name = font_manager.FontProperties(fname = font_location).get_name()

matplotlib.rc('font', family = font_name)
plt.plot([1,2,3,4])
plt.xlabel("x축")
plt.show()
