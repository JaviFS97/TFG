// Firebase
import {auth} from '@/firebase'

/**
 * Represents the generic class for users.
 */
export default class User{
    /**
     * Constructor for generic users.
     * All of them have an email and a password.
     * @param {String} email 
     * @param {String} password 
     */
    constructor(email, password){
        this.email = email;
        this.password = password;
    }

    /**
     * Register a user in Auth Firebase.
     * @returns {Promise<UserCredential>} 
     */
    async createUserAuth(){
        var credentials = await auth.createUserWithEmailAndPassword(this.email, this.password);
        return credentials;
    }

    /**
     * Register a user in Auth Firebase.
     * @returns {Promise<UserCredential>} 
     */
    async sendEmailVerification(){
        var credentials = await auth.currentUser.sendEmailVerification()
        return credentials;
    }

    /**
     * This method authenticates the generic user.
     * @returns {Promise<UserCredential>} 
     */
    async login(){
        var credentials = await auth.signInWithEmailAndPassword(this.email, this.password)
        return credentials 
    }
}