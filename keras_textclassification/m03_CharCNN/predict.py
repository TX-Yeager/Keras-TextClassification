# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/12 14:11
# @author   :Mo
# @function :

import pathlib
import sys
import os

project_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent)
sys.path.append(project_path)

import numpy as np

from keras_textclassification.conf.path_config import path_embedding_random_char
from keras_textclassification.conf.path_config import path_model_fast_text_baiduqa_2019
from keras_textclassification.etl.text_preprocess import PreprocessText
from keras_textclassification.m03_CharCNN import CharCNNGraph as Graph

if __name__=="__main__":
    hyper_parameters = {'model': {   'label': 17,
                                     'batch_size': 64,
                                     'embed_size': 30,
                                     'filters': [2, 3, 4], # 这里无用
                                     'filters_num': 30,
                                     'channel_size': 1,
                                     'dropout': 0.5,
                                     'decay_step': 100,
                                     'decay_rate': 0.9,
                                     'epochs': 20,
                                     'len_max': 50,
                                     'vocab_size': 20000, #这里随便填的，会根据代码里修改
                                     'lr': 1e-3,
                                     'l2': 1e-6,
                                     'activate_classify': 'softmax',
                                     'embedding_type': 'random', # 还可以填'random'、 'bert' or 'word2vec"
                                     'is_training': False,
                                     'model_path': path_model_fast_text_baiduqa_2019,
                                     'char_cnn_layers': [[50, 1], [100, 2], [150, 3],[200, 4], [200, 5], [200, 6],[200, 7]],  # large
                                     # [[25, 1], [50, 2], [75, 3], [100, 4], [125, 5], [150, 6]])  # small
                                     'highway_layers': 1, # large:2; small:1
                                     'num_rnn_layers': 1, # 论文是2，但训练实在是太慢了
                                     'rnn_type': 'GRU', # type of rnn, select 'LSTM', 'GRU', 'CuDNNGRU', 'CuDNNLSTM', 'Bidirectional-LSTM', 'Bidirectional-GRU'
                                     'rnn_units': 650,  # large 650, small is 300
                                     'len_max_word': 26,
                                     },
                        'embedding':{ 'embedding_type': 'random',
                                      'corpus_path': path_embedding_random_char,
                                      'level_type': 'char',
                                      'embed_size': 30,
                                      'len_max': 50,
                                      'len_max_word': 26
                                      },
                         }

    pt = PreprocessText
    graph = Graph(hyper_parameters)
    graph.load_model()
    ra_ed = graph.word_embedding
    ques = '你好呀'
    ques_embed = ra_ed.sentence2idx(ques)
    pred = graph.predict(np.array([ques_embed]))
    pre = pt.prereocess_idx(pred[0])
    print(pre)
    while True:
        print("请输入: ")
        ques = input()
        ques_embed = ra_ed.sentence2idx(ques)
        print(ques_embed)
        pred = graph.predict(np.array([ques_embed]))
        pre = pt.prereocess_idx(pred[0])
        print(pre)
