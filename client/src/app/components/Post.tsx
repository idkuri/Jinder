"use client"
import React, {useState} from 'react';
import Image from 'next/image'
import "../styles/post.css";
import "../styles/globals.css"

interface PostProps {
    username: string;
    content: string;
    createPostFunc: () => void
}

const Post: React.FC<PostProps> = ({ username, content, createPostFunc }) => {
    const [mode, setMode] = useState(0)

    function renderButtons(): JSX.Element {
        return (
            <>
                <button className="btn text-xl">Like</button>
                <button className="btn text-xl" onClick={() => {createPostFunc()}}>Create Post</button>
            </>
        )
    }
    return (
        <div className="post-element">
                <div className='user-profile'>
                    <Image src="https://www.svgrepo.com/show/347900/person.svg" width={100} height={100} alt="Person"></Image>
                    <p>{username}</p>
                </div>
                <div className='post-content'>{content}</div>
                <div className='footer'>
                    {renderButtons()}
                </div>
        </div>
    );
};

export default Post;