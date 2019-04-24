# Still Working

## Background
My diploma project is to make some improvements on [DeepPoly](https://github.com/eth-sri/eran)
and use it to test some other DNNs.

## First Step

### Ideas:
Since DeepPoly only support MNIST and CIFAR-10 for now, l want to generalize its code so that
it can handle more Image-Classify Problems.

So l trained a CNN using the dataset from [here](http://www.robots.ox.ac.uk/~vgg/data/) for testing when l was refactoring 
code. To simplify the training process, l only use six kinds of flowers. Another reason for the 'six' is
that l borrowed the architecture from [Coursera](https://www.coursera.org/learn/convolutional-neural-networks/home/welcome).
So thanks Andrew NG and his team here.

You also can download the entire `dataset`(17flowers.tgz) there.
### Results:
l think the results so far have met expectations. And l also adjusted the code logic in `analyze.py` to improve performance.
You can find the final version of `__main__.py` and `analyzer.py` in the root directory of `DeepPoly`. 
## Second Step
### Ideas:
Only in safety critical domains can DeepPoly show its importance. So 
l want to use it to test autonomous driving network. And l 
use the models that are mentioned in <https://arxiv.org/abs/1802.02295>
and also open in [github](https://github.com/udacity/self-driving-car).
But l am encountering great difficulty because these networks are not used
to classify images, but used to predict driving-angles which means they will only
generate a real value. So l will change the code in DeepPoly so that it 
can handle these networks.`Wish me luck`.
### Results:
l think that l make DeepPoly deal with Autumn successfully. You can find the improved code in `DeepPoly`.
But the results are terrible. And l also try the [LeNet-5](https://github.com/ganyc717/LeNet), the results are also ordinary. 
Because of its incompleteness l can't draw an accurate conclusion.
## Third Step
l read other the papers about testing techniques of DNN's robustness. They will find the DNN's 
`minimum abversarial distortion`. So l combined the DeepPoly with Binary Search, the new `__main__.py` in `Binary_Search`
can be used to find it.
## Fourth Step 
l have developed a Visual System based on DeepPoly. Specifically, I developed a website By Vue and Django.
You can find the main code in `VisualSystem` directory. And l trained an CNN again which l learned from [here](https://github.com/ameyas1/CNN_Medical_Pneumonia).
Although it doesn't have a `star` but l think DeepPoly can't handle the big DNNs used in the medical field.
You can find the training code and sth else in `ChestNet` directory.
## Finally
Soon l will upload my paper here and you can check my results. But l think it's meaningless because you konw, the problem about testing
the robustness of DNNs are NPC problems. And related techniques are just getting started. 