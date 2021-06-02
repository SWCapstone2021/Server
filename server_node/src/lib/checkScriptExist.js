import Video_info from '../model/VideoInfo';

const checkScriptExist = async (ctx, next) => {
    try {
        const { video_id } = ctx.request.body;
        const script_exists = await Video_info.findByVideoId(video_id);
        if(script_exists) {
            ctx.body = 'Subscription Already exists'
            return;
        }
        else 
            return next();
        
    } catch (e){
        ctx.throw(500, e);
    }
}

export default checkScriptExist;