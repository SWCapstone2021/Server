import mongoose from 'mongoose';

const { Schema } = mongoose;

const ScriptSchema = new Schema({
    text: String,
    start: String,
})

const videoInfoSchema = new Schema({
    video_id: String,
    title: String,
    scriptions: [ScriptSchema],
    summarization: String
});

videoInfoSchema.statics.findByVideoId = function (video_id) {
    return this.findOne({ video_id });
}

const VideoInfo = mongoose.model('Video_Info', videoInfoSchema);

export default VideoInfo;