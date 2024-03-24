"use client"
import React, {useEffect, useState} from 'react';
import Image from 'next/image'
import "../styles/post.css";
import "../styles/globals.css"

interface PostProps {
    id: number;
    username: string;
    content: string;
    createPostFunc: () => void
}

const Post: React.FC<PostProps> = ({ id, username, content, createPostFunc }) => {
    const [mode, setMode] = useState(0)
    const [liked, setLiked] = useState(false)

    async function handleLikeButton() {
        const response = await fetch("/api/like", {
            method: "POST",
            body: JSON.stringify({id: id})
          })
    }

    useEffect(() => {
        getLike()
    })

    async function getLike() {
        const response = await fetch("/api/getLike", {
            method: "GET",
          })
          if (response.status == 200) {
            const responseData = await response.json()
            setLiked(responseData)
        }
    }
 
    function renderButtons(): JSX.Element {
        if (liked) {
            return (
            <>
                <button className="btn text-xl" onClick={handleLikeButton}>Liked</button>
                <button className="btn text-xl" onClick={() => {createPostFunc()}}>Create Post</button>
            </>
            )
        }
        else {
            return (
                <>
                    <button className="btn text-xl" onClick={handleLikeButton}>Like</button>
                    <button className="btn text-xl" onClick={() => {createPostFunc()}}>Create Post</button>
                </>
            )
        }
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