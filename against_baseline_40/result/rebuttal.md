# General

We sincerely thank all the reviewers to their valuable and helpful comments on our works. We are happy to see that most of the reviewers agrees on the novelty of the proposed task and our effort that we have spent on the experiments. And we also appreciate our reviewers for finding the weakness of the paper.

Still, we notice that most of the reviewers have show their concern about the generalization ability of the proposed method and the difficulty of the task on the chosen dataset. So, we want to first clarify a little bit more on the background of the task so called "conditional foley generation", its importance and difficulty. More specific questions and concern for each reviewer will be addressed in the specific comments.

## Task background and its importance

As we have mentioned in the abstract of the paper, sound designers are frequently facing the challenge to design a specific sound effect for a given video clip. The general procedure includes the following steps:

1. *Spotting*: The sound designer will spot the location where sound effects need to be added, which will generally be a shorter video clip of repeated and similar sound events, e.g., footsteps, sword fight, hitting/scratching specific objects.

2. *Retrieval*: The sound designer will find the desired sound effect in their own library that suits the scenario of the spotted video clip.

3. ***Processing & Adapting***: However, since the sound effect in the library is normally recorded in a condition that is far different from the target video clip, the sound designer will have to spend hours of work on adjusting the timing and timbre of the selected sound effect to make it align perfectly with the video clip.

And our work is mainly focused on addressing the most complicated and tedious part of the sound designer's workflow. This task is very different from the general *conditional sound generation* task, as mentioned by reviewer rbft, since it not only asks the generated sound to follow the required timbre but also asks it to synchronize with the given video. We believe this is a much more difficult but novel and interesting task in this area. In fact, we didn't find works that can address the proposed task to the best of our knowledge.

## Concerns about the dataset

It seems that all of the reviewers have shown their concern about the dataset used in the paper. Reviewers are concerned that the video in the Greatest Hits dataset may be too straightforward and will simplify the task to extend and, therefore, cannot represent the general situation in a more realistic situation. We are happy to see that our reviewers are helping address the potential problems of the work, and we would like to include more discussion on this in the updated version of the paper.

However, we have to strengthen that the proposed task is new to this area, and there are few relevant datasets. General sound effect dataset, such as FSD50K (Fonseca et.al, 2020), only contains audio waveform but not corresponding video. While the widely known video dataset such as VGG-Sound (Chen et.al, 2020) and AudioSet (Gemmeke, 2017) only provides videos with non-negligible background noise and may contain irrelevant sounds like human speaking, or sound effect after processing. All these drawbacks make them not the ideal choice for our task, which requires clean and repeated sound events as mentioned in the previous sound designer's workflow.

From this perspective, we believe the Greatest Hits dataset is one of the best datasets that fit with the task definition. Moreover, the dataset actually contains the abundant sound event that includes more than 30 materials. As a matter of fact, the sound effects in the sound designer's library will be very close to what we have in the Greatest Hits dataset but may contain a larger range of the sound type.

Considering the fact that this is a new task with little work to learn from, our work has taken the first step, as well as a solid step toward solving this problem in a realistic setting. Looking back at the development of image generation, when we are amazed by the Imagen and DALL-E, we also should not forget how it was at the early stage.


## How will the proposed training paradigm work in a realistic scenario?

As many of the reviewer points out, the proposed training paradigm may not work well on a more realistic scenario like a movie clips, we believe it is necessary to illustrate how things will be when sound designer integrate our proposed method into their workflow.

Still, the sound designer will need to work on the creative portion of *Spotting* and *retrieval* task, we give user control on where they want to add the sound effect and how they want it sounds like. The spotted silent video clip $v$ and sound effect with corresponding video $(a', v')$ will be the output of this part. The target video $v$ will contain certain repeated actions and the conditional pair $(a', v')$, which comes from the sound effect library, will also have such characteristic of repeated sound events.

Then, our model will take these two input and generate a sound $a_{gen}$ that aligns with action in $v$ but sound like $(a', v')$.

Even if for a more realistic scenario, the assumption about the input will still hold, and the proposed training paradigm: learning the timbre from $(a', v')$ and align it with $v$ can also work.


## Concerns about the "Onset transfer" baseline

As both reviewer PTLK and 2KN7 mentioned, the "Onset transfer" baseline outperform our full model in multiple metrics, and it is worth a discussion on whether this indicates that the task can be solved with a simpler "copy and paste" model. 

As a matter of fact, we believe the success of the "Onset transfer" baseline is, unfortunately, due to the limitation of the dataset. As we have mentioned in the paper, the proposed method is only trained a a dataset with various of hit/scratch sound events, this results that a simple "copy and paste" model can take advantage on this characteristic, and "copy" sound from the conditional pair and "paste" to the output and therefore obtain a better performance on certain metrics.

However, we also want to strengthen that this baseline also fails when the action type is mismatch between target and condition video. As shown in the Table 2 of the paper, the "Onset transfer" baseline's classification accuracy have dropped from 69.0% to 44.7% when the actions are mismatch, while our full model shows a much better performance of 59.2% in the mismatch case. This indicate the proposed method will generalize better when plugged into a scenario with more abundant sound classes. 

Moreover, one recent experiment we conducted also shows that the "Onset transfer" baseline is not as good as it looks like. We utilize the onset detection function in the librosa library to evaluate the both the *number* and *timing* of onsets in the generated sound with respect to the original sound (it is valid to do so since timbre of the sound does not influence the onset). We evaluate both targets in terms of accuracy

1. Number of onset: Only when the generated sound have the same number of onset as the target video, it is considered as correct.
2. Timing of the onset: we take the mean value of the ratio of the matched onsets in the generated sound with respect to the original sound. An onset in the original video can be matched with an onset in the generated sound only if the time difference between them is with in range $[-0.1, 0.1]$ second. Once an onset in the generated sound find its match in the original audio, we remove it for later matching.

And here is the results:
|Methods|#Onset(Acc)|Timing of Onset(Acc)|
|:-:|:-:|:-:|
|Ours (Full)|	**0.2904**|	0.6831|
|Onset transfer|	0.2199|	0.7068|
|no cond|	0.2337|	0.6624|
|no cond vis|	0.2526|	0.6384|
|no aug|	0.2749|	0.6733|
|style transfer|	0.1649|	**0.7407**|
|outside cond|	0.2612|	0.6641|

It turns out that our  method does the best on counting the onsets, while the "Onset transfer" may good at the synchronization task, which it is explicitly trained to do so, our method shows a really close performance on this task. It is worth to notice that the style transfer baseline has a best performance on the timing task since it uses the original sound during the generation, which naturally leads to a high accuracy.

We also notice a generally low accuracy in counting the onsets. After checking the data, we notice that there are a large number of "tail sound", which is the latter part of a previous sound event that presents in the sampled clips. For these "tail sound", the corresponding action is already ended before the clip, but the sound will still be counted in by the librosa function. But for the proposed model that generate the sound based on actions, these sound event will not be noticed. We believe this is the reason of a low accuracy in the number of onset detection task.

The results above can help illustrate how will the "Onset transfer" baseline fails when we generalize to a more realistic scenario. We will happy to include further discussion on these experiment in the updated version of the work.

# PTLK

We the reviewer for the insightful review. We arrange the review in such a way that we hope to address all the questions and concerns you have mentioned.

> The data chosen for this task is narrowly constrained...

Please refer to the "Concerns about the dataset" section in the general comment for this.

> The results are not better for the proposed method compared to a simpler baseline.

Please refer to the "Concerns about the "Onset transfer" baseline" section in general comment.

> How the confidence intervals are calculated

We evaluate the confidence intervals with following equation:

$$\overline{X} \pm z_{\alpha/2} \times \frac{\sigma}{\sqrt{N}}$$

where, $X$ is all the feedback, $z_{\alpha/2} = 1.96$ for $95\%$ confidence interval case, $\sigma$ is the standard deviation, and $N$ is the overall sample size, which is the population for different baseline tested through out the evaluation.

Meanwhile, thanks to your reminder, we notice that we have used a wrong population number in the previous confidence interval calculation, where we used 200 for all cases, but it should be larger than that in the fact. Since we have 200 set of feedback, and each contains 21 randomly sampled video pairs (different for each set of test). After removing 5 practice question and 1 sentinel case, there are $15 \times 200 = 3000$ samples in total. Since we have 7 baselines, then each baseline should have a population approximately equal to $3000 / 7 \approx 429$ samples. The actual population for each baseline is different due to random sampling. The updated confidence interval is presented in the table below:

|Method|Material Chosen(%)$\uparrow$|Sync. Chosen(%)$\uparrow$|
|:-:|:-:|:-:|
|Style-transfer|$11.4\pm 2.9$|$11.0 \pm 2.8$|
|Onset transfer|$64.5\pm 4.6$|$58.2\pm 4.7$|
|SpecVQGAN|$18.0\pm 3.6$|$19.6\pm 3.7$|
|no conditional|$34.5\pm 4.6$|$43.0 \pm 4.8$|
|no cond. video|$46.0\pm4.7$|$44.3\pm 4.7$|
|no augmentation|$50.0\pm 4.9$|$49.3\pm 4.9$|
|train w/ rand. cond.|$45.7\pm 4.7$|$48.2\pm 4.7$|
|Full|$50.0\pm 0.0$|$50.0\pm 0.0$|

In this case, most of the comparison locates outside the confidence interval and we now have stronger confidence on our results. 

> whether the 21 examples are the same for all subjects or not

As mentioned above, no. these 21 examples are randomly sampled from 7 sets of 582 pairs of target-condition combination in the test set. From that perspective, the population size is not as big as it looks like, and this is also why the confidence interval looks large even after fixing the problem.

> Can you explain how your method would have to be different in order to apply to a real foley problem, given training data from, say, movies?

Please refer to "How will the proposed training paradigm work in a realistic scenario?" section in the general comments

> Why no-conditioning baseline also fails on the "matching materials" task. how can you know the model is not just hobbled so that it needs the extra input in order to synthesize?

Since the no-conditioning baseline has no access to condition clips, it will naturally fail on generating a sound that matches the conditioning material. And as for the synchronization task, the new experiment in "Concerns about the "Onset transfer" baseline" section in the general comments suggest that the no-conditioning baseline is also good at the synchronization task, but not as good as the full model. Furthermore, we believe that the extra conditional audio-visual pair can actually boost the performance on synchronization since the model may learn about the analogy from the conditional pair to the target pair.

> What they should be making clear is that the training paradigm and model architecture are not likely to perform well in any broader domains, even if trained on data from those domains. 

As mentioned in the "How will the proposed training paradigm work in a realistic scenario?" section in the general comments, we have a strong reason to believe that the proposed paradigm can also work on more general and realistic scenarios with respect to the defined task.


# 2KN7

We thank the reviewer's detailed and valuable comments on our works. It is very helpful to have those detailed concerns and question addressed for us to make the work better. The questions about writing part will be put to the end.

> I am not convinced the system detects the onsets very well.

As shown in the new experiment result in the "Concerns about the "Onset transfer" baseline" of the general comment, the proposed method actually shows a promising onset detection ability even comparing with the "Onset transfer model", which was explicitly train on this task. It is reasonable for us to believe that the model can detect the onsets in the video correctly.

> I'm not sure if the training scheme is an instance of "self-supervision"

We didn't any label during the training procedure. The VQ-GAN model is supervised with its own spectrogram, and the transformer is supervised with the token of the original audio provided in the video, which does not require additional label as well.

> L40: ..[and duration] → Really? I don’t think so, both from the concept of the system and the experiment results.

The duration here refers to the duration of the sound events. As shown in the Figure 4 and 5, different type of action actually results in a sound even of different length, and the model should take care of this and generate a sound with correct duration.

> L94: [from each] → What is each source here?

from target video and conditional audio-visual pair.

> L103: [exploits the facts that..] → This fact is true for the dataset. But - is it actually true for more realistic videos? If it’s not, then this fact matters only when the propose dataset was used, i.e., it’s not a part of the real problem.

As we have mentioned in the "Task background and its importance" section of the general comment, the realistic workflow of the sound designer do involves design sound events for spotted video clips with repeated action/sound event, which also follow the assumption we proposed in the L103.

> L127: [perceptual loss [28]] → I know the name of the loss proposed in [28] is ‘perceptual loss’. But I believe this is an unfortunate name, especially when the name is used in a different domain. How is it perceptual, especially when it comes to audio? We’d need some explanation here.

we were following the established terminology in previous works including the SpecVQGAN (Iashin et.al, 2021).

> L201: [Style Transfer method. ..Ulyanov [45]] I have to note that [45] is a really bad baseline; one of the many, poorly designed attempts of trying to use Gatys et al. to spectrograms, not something that would be able to be accepted in any rigorous conference.

We decide to hire this baseline since the overall idea is close, i.e., "borrowing sound style from condition and apply to target". However, as mentioned before, this is a novel task with little works to refer, we are afraid that there are not many choices we have. Happy to discuss possible alternatives!

> Table 1: I’d like more discussion on why [No cond.] configuration was done.

The [No cond.] configuration is design to simulate a stronger version of SpecVQGAN (Iashin et.al, 2021) with a better visual backbone, and it is also important to have it demonstrate the necessity of conditional pair on this task. Without conditioning, the model generally do a poor job in the timbre tasks.

> ... it’ll be really important to have analysis and comparison around it.

Please refer to the "Concerns about the "Onset transfer" baseline" section in the general comment. The success of the "Onset transfer" baseline is largely comes from the characteristic of the dataset, and once we move to a sound effect dataset with much more abundant sounds, its failure is predictable from its nature.

> ... But, would the proposed system work any better? If you think so, please provide some reason for the thought.

Please refer to the "How will the proposed training paradigm work in a realistic scenario?" section of the general comment.

## Writing issues

We appreciate for the reviewer's detailed comments on the writing mistakes of the paper. And we will follow those comments and update in the newer version of the paper.

# XZ77

We appreciate the reviewer for pointing out the novelty and importance of the proposed task and other insightful comments. They are really helpful for us to make it a better work. Still, we will try our best to address the questions in the following comments.

>  The proposed task of conditional Foley is somewhat niche, and perhaps of somewhat limited interest.

Please refer to "Task background and its importance" section in the general comments. We believe our work will be an important step to help address the complicated and tedious work for the sound designers, and allow them to spend more time on the creative tasks.

> ... the video demos, especially for randomly-selected examples, show a somewhat inconsistent behavior...

Thanks for pointing this out, and indeed, there might be some failure cases in the randomly sampled result. But in general, as shown in the Table 1 and 2, our model still performs pretty well on the automated metrics overall.

> ... the Greatest Hits is a pretty limited domain of sounds...

We have to agree that the richness of the sound event in the Greatest Hits dataset is limited. But it is still one of the best choice we can have considering this is the very first try on this task. Would happy to discuss any possible alternative solution to improve from the dataset aspect!

> What is the performance of the classifier on the input video soundtracks? ...

We do provide these two number in the section D of the supplementary. And the validation accuracy on the material task is 75.6% and the accuracy on the action prediction task is 92.0%. Besides that, we think the key to this automated metric is to employ a classifier with consistent behavior on different input, since we are evaluating between different baseline with the classifier, rather than comparing it with others. Still, we agree that it will be good to have these number in the main paper.

## Writing issues

We also thank the reviewer for pointing out the typos and problems in the paper writing, they are really helpful and we will fix those typo in the updated version.

# rbft

We sincerely thank the reviewer for providing the comments, and noting our efforts in the experiment part. And we also believe that there are questions and concerns that we can further clarify. Please do let us know if there is any concerns that we were missing in the comments. Happy to provide further feedback if required!

## Perhaps the authors can clarify how this specific problem is important and how it might be used in a Foley artist workflow? & The difference from existing audio generation methods.

For most of the concern on this, we strongly suggest the reviewer to refer to the general comment. 

Additionally, we want to strengthen that the existing video -> audio generation ML method with controllable parameters is that our work fit better in the actual workflow for the sound designer. And we believe it is the very first try on this problem to the best of our knowledge. Although previous works in the "conditional audio generation" did a impressive contribution to the community in terms of generating high fidelity sound, they either focus on generating sound that is far from sound effect, i.e., speech or music, or does not allow user to control the timbre explicitly. Our method allows the user to choose what the want the sound to be like and reduce the work for the sound designer on process and adjusting the sound's timing and detail. We believe it is important to "put someone back in the loop" for such a task that requires human's creative mind to select the best fit sound effect. Our automated system is designed to overcome the most complicated part of the sound designer's job.

> The authors address the fact that the model was only trained and evaluated on this drumstick dataset

As mentioned in the "Concerns about the dataset" section in the general comment, although we the Greatest Hits dataset is one of the best dataset that we can use for the tasks and our experimental result are therefore limited due to this, multiple experiment results including material/action classification result when mismatch and onset prediction result demonstrate the potential of the proposed method in the broader area that is closer to the realistic scenario.
