// get 자막 전달하기 :: 논의 필요

// post 자막이 없다 ==> 자막 다운 받기
// 요청온 아이디와 일치하는 비디오 id가 있는가?
// 1. 없으면 다운 받는다. ==> 가공해서 ==> 완료된 데이터를 전달
// 있으면 기존에 존재하는 것을 전달.
/*
 POST /api/scripts
{
    video_id: 'id'
}

*/
import Video_info from '../../model/VideoInfo';
import get_script from '../../lib/get_script';

function Ctrl_F(keyword, script) {
    let TimeStamp = [];
    //let TimeStamp = new Map();
    let splited_keyword = keyword.split(" ");

    for (let per_data of script) {

        let line = per_data['text'].replace('\n', '');

        for (let _keyword of splited_keyword) {

            if (line.includes(_keyword)) {
                TimeStamp.push(
                    {
                        script: line,
                        start: per_data['start'],
                        id: per_data['_id']
                    });
            }
        }
    }

    TimeStamp = TimeStamp.filter((v, i, a) => a.findIndex(t => (t.id === v.id)) === i);

    return TimeStamp;
}


export const download_script = async (ctx) => {

    try {
        const { video_id } = ctx.request.body;
        const script_exists = await Video_info.findByVideoId(video_id);
        if (script_exists) {
            ctx.body = script_exists;
            return;
        }
        else {
            const result = await get_script(video_id).then(script =>
                JSON.parse(script));

            const video_info = new Video_info({
                video_id,
                title: result["title"],
                scriptions: result["transcript"],
            });

            try {
                await video_info.save();
                ctx.body = video_info;
            } catch (e) {
                ctx.throw(500, e);
            }
        }
    } catch (e) {

        ctx.throw(500, e);
    }
}

/* ctrl + F */
export const find_word = async (ctx) => {

    try {
        const { video_id, keyword } = ctx.request.body;

        const script_exists = await Video_info.findByVideoId(video_id);

        let result;

        if (!script_exists)
            ctx.throw(500, new Error("No subs"));

        else {
            result = Ctrl_F(keyword, script_exists['scriptions']);
        }

        ctx.body = {
            video_id,
            keyword,
            result
        };

    } catch (e) {
        ctx.throw(500, e);
    }
}

/* export const send_script = async (ctx) => {

    const { video_id } = ctx.request.body;
    let video_script_list = [];

    for(let i = 0; i < video_id.length; i++){
        let id = video_id[i];
        const search_result = await Video_info.findByVideoId(id);
        video_script_list.push(search_result);
    }

    try {
    ctx.body = video_script_list;
    } catch(e) {
        ctx.throw(500, e);
    }
} */
