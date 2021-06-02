import Video_info from '../../model/VideoInfo';
import get_script from '../../lib/get_script';
import axios from 'axios'

function unrollScript(script) {

    let unrolledScript = "";
    const scripts = script.scriptions;

    for(let i of script)
        unrolledScript += scripts[i].text+ " ";
    return unrolledScript;
}

function Frequency(keyword, script){
    let TF = 0,
        ILF = 0,
        TF_IDF = 0; 
    
        for(let line of script){
            line = line['text'];
            if(line.includes(keyword))
                ILF++;
        }
   /*  for (let line in script){
        line = line['text'];
        if (keyword in line)
            ILF += 1;
        } 
    */

    /* for (let word in script){
        word = word['text'];
        if (keyword in word)
            ILF += 1;
    } */
    
    if (ILF !== 0)
        TF_IDF = ILF * Math.log(script.length / ILF)

    return TF_IDF.toFixed(2)
} 


export const calculate_credibility = async (ctx) => {
    const { video_id, keyword } = ctx.request.body;
    let video_script_list = [];

    try {

    for (let _id of video_id){
        let script_exists = await Video_info.findByVideoId(_id);

        if(!script_exists) {
            try {
            script_exists = await get_script(_id).then( script =>
                JSON.parse(script));
            } catch(e) {
                video_script_list.push({
                    video_id: _id,
                    credibility: "No subs"
                });
                continue;
            }
            const video_info = new Video_info({
                video_id : _id,
                scriptions: script_exists['transcript'],
            });
            
            script_exists = video_info;

            try {
                await video_info.save();
            } catch (e) {
                ctx.throw(500, e);
            }    
        }

        let script_data = script_exists['scriptions'];

        let tmp_result = {
            video_id: _id,
            credibility: Frequency(keyword, script_data)
        }

        video_script_list.push(tmp_result);
    }
    ctx.body = {
        keyword,
        result: video_script_list
    }

    } catch(e) {
        ctx.throw(500, e);
    }
}


export const QAsystem = async (ctx) => {
    const { video_id, question } = ctx.request.body;
    const find_result = await Video_info.findByVideoId(video_id);
    let unrolledScript = unrollScript(find_result);
    /* 모델에 자막 정보와 question을 보냄 */

    ctx.body = unrolledScript;
    /* Answer 결과를 body에 실어서 전달함.*/
}

export const Summarization = async (ctx) => {

    const { video_id } = ctx.request.body;
    let find_result = await Video_info.findByVideoId(video_id);
    let unrolledScript;

    /* 이미 요약 결과가 있으면 요약한 내용을 보냄. */
    if(find_result.summarization != undefined){
      ctx.body = {
	      video_id,
	      summarization: find_result.summarization
      };    
    }

    else {
	await axios.post('http://202.30.30.3:5678/summarization', 
		{ video_id })
	    	   .then( response => {
			   ctx.body = response.data;
		   })
	    	   .catch( e => {
			   ctx.throw(500, e);
		   });
    }


    /* 없으면 만들어야 함. 모델에  자막을 보낸다*/

    /* 요약 결과를 저장하고, 결과로 보낸다.*/
}
