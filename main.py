import shiping
import os
import threading
import time
import concurrent.futures

if __name__ == '__main__':
    txt='"震惊！这款产品竟然让我忘了前任的速度，比找到新欢还快！"朋友们，别眨眼，这不是科幻大片的预告，而是我们产品的魅力宣言。想象一下，拥有了它，就如同解锁了一项超能力——瞬间提升生活品质，让困扰你的种种问题像前男友/女友一样，迅速淡出你的世界！我们的产品，不仅拥有硬核的实力，更有着体贴入微的人性化设计，让你一用就上瘾，再也回不去！它的魔力在于，不仅能解决实际需求，还能唤醒你内心深处对美好生活的向往和追求。'
    shiping.run('output1',txt)
