# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/4 20:26
@Auth ： xiaolongtuan
@File ：gen_hard.py
"""
import time

from GPT4_agent import run_conversation_gen, run_conversation_change

if __name__ == '__main__':
    start_time = time.time()
    # print(run_conversation_gen(model="gpt-4-1106-preview",
    #                            require_path="networks/hard_gen.md",
    #                            network_root="networks/hard",
    #                            tools=["utils/toolsjson/config_update.json"],
    #                            device_list=["as1core1", "as1border1", "as1border2",
    #                                         "as3core1", "as3border1", "as3border2",
    #                                         "as2core1", "as2core2", "as2border1",
    #                                         "as2border2", "as2dist1", "as2dist2"],
    #                            human_in=False))
    #
    # gen_end = time.time()
    # gen_time = gen_end - start_time
    # print(f"Gen Time: {gen_time} seconds")

    # 修改配置文件
    print(run_conversation_change(model="gpt-4-1106-preview",
                                  require_path="../utils/test/policy_test2.txt",
                                  network_root="networks/hard",
                                  tools=["utils/toolsjson/config_update.json"],
                                  human_in=False))
    end_time = time.time()

    change_time = end_time - start_time
    print(f"change Time: {change_time} seconds")
